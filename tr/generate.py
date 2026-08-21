"""Prompt assembly and OpenRouter calls."""
import os
import re
from pathlib import Path

PROMPTS = Path("prompts")


def load_dotenv(path=".env"):
    """Read KEY=value lines from .env into the environment, if present.

    Six lines of stdlib instead of a dependency. Real environment variables win,
    so an explicitly exported key always overrides the file. `.env` is gitignored.
    """
    p = Path(path)
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        os.environ.setdefault(key.strip(), val.strip().strip("'\""))


def client(cfg):
    from openai import OpenAI

    load_dotenv()
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise SystemExit(
            "No OPENROUTER_API_KEY found. Either export it, or put this in a "
            "file called .env next to config.yaml:\n\n"
            "    OPENROUTER_API_KEY=sk-or-...\n\n"
            ".env is gitignored, so it will not be committed."
        )
    return OpenAI(base_url=cfg["base_url"], api_key=key)


def llm(cl, model, system, user, max_tokens=None):
    kwargs = {"model": model, "messages": [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]}
    if max_tokens:
        kwargs["max_tokens"] = max_tokens
    resp = cl.chat.completions.create(**kwargs)
    return resp.choices[0].message.content or ""


def prompt(name):
    return (PROMPTS / name).read_text(encoding="utf-8")


def fill(template, values):
    """Replace {{key}} placeholders. Unfilled ones stay visible on purpose."""
    for k, v in values.items():
        template = template.replace("{{" + k + "}}", str(v) if v else f"[NEEDS: {k}]")
    return template


def section(title, body):
    if not body:
        return f"\n\n===== {title} =====\n(not supplied)\n"
    return f"\n\n===== {title} =====\n{body}\n"


def distill_style(cl, model, items):
    """One-time: turn the whole corpus into style-guide.md."""
    body = "".join(section(f"SOURCE: {p.name}", text) for p, text in items)
    return llm(cl, model, prompt("style_guide.md"),
               "Here is the material.\n" + body)


def job_line(ctx):
    """One line saying what this run actually is, for the questions prompt."""
    mode, pos = ctx.get("mode") or "new", ctx.get("position") or "middle"
    if mode in ("revamp", "repurpose"):
        return (f"{mode.upper()} of the existing session at position "
                f"{ctx.get('at')}: {ctx.get('target_title')}")
    where = {
        "first": "as the FIRST session of the course",
        "last": "as the LAST session of the course",
    }.get(pos, f"inserted after position {ctx.get('after')}")
    return f"NEW session, {where}"


def build_questions(cl, model, ctx):
    system = fill(prompt("questions.md"), {"topic": ctx["topic"]})
    user = (
        f"Course: {ctx['course']}\nSession topic: {ctx['topic']}\n"
        f"Job: {job_line(ctx)}\n"
        + section("CURRENT DOC TO REVISE", ctx.get("target_doc"))
        + section("AUTHOR'S CHANGE BRIEF", ctx.get("change_brief"))
        + section("PREVIOUS SESSION TR DOC", ctx["prev_doc"])
        + section("NEXT SESSION TR DOC", ctx["next_doc"])
        + section("STUDENT KNOWLEDGE BASELINE (everything the learner already knows)",
                  ctx.get("baseline"))
        + section("HOUSE STYLE GUIDE", ctx["style"])
        + section("RESEARCH NOTES", ctx["research"])
    )
    return llm(cl, model, system, user)


def block(kind, name):
    """A mode or position brief. Unknown names fail loudly rather than silently
    producing a doc with no instructions for this run."""
    p = PROMPTS / kind / f"{name}.md"
    if not p.exists():
        have = ", ".join(sorted(x.stem for x in (PROMPTS / kind).glob("*.md")))
        raise SystemExit(f"No {kind} brief named {name!r}. Have: {have}")
    return p.read_text(encoding="utf-8").strip()


def write_doc(cl, model, ctx, answers):
    system = fill(prompt("tr_doc.md"), {
        "course": ctx["course"],
        "topic": ctx["topic"],
        "previous_session": ctx["prev_title"] or "none -- this is the first session",
        "next_session": ctx["next_title"] or "none -- this is the last session",
        "learner_profile": ctx.get("learner_profile"),
        "session_produces": ctx.get("session_produces"),
        "mode_brief": block("modes", ctx.get("mode") or "new"),
        "position_brief": block("positions", ctx.get("position") or "middle"),
    })
    user = (
        section("STUDENT KNOWLEDGE BASELINE (everything the learner already knows, "
                "across every earlier course -- do not re-teach any of it, and do "
                "not use a term from outside it without defining it)",
                ctx.get("baseline"))
        + section("HOUSE STYLE GUIDE", ctx["style"])
        + section("PREVIOUS SESSION TR DOC (verbatim)", ctx["prev_doc"])
        + section("NEXT SESSION TR DOC (verbatim)", ctx["next_doc"])
        + section("SOURCE MATERIAL: PREVIOUS SESSION SLIDES", ctx.get("prev_ppt"))
        + section("CURRENT DOC TO REVISE", ctx.get("target_doc"))
        + section("AUTHOR'S CHANGE BRIEF", ctx.get("change_brief"))
        + section("HOOK FOUNDATION (what the learner arrives knowing)",
                  ctx.get("hook_foundation"))
        + section("RESEARCHED SOURCES", ctx["research"])
        + section("AUTHOR'S ANSWERS TO YOUR QUESTIONS", answers)
    )
    return llm(cl, model, system, user)


def self_check(cl, model, doc, prev_doc, research, baseline=None):
    user = (
        section("THE DOC UNDER REVIEW", doc)
        + section("STUDENT KNOWLEDGE BASELINE", baseline)
        + section("PREVIOUS SESSION TR DOC", prev_doc)
        + section("SOURCES AVAILABLE TO THE WRITER", research)
    )
    return llm(cl, model, prompt("self_check.md"), user)


def split_trailing_blocks(doc):
    """Pull SOURCE ISSUES / OPEN MARKERS / CHANGES MADE off the end of the doc."""
    m = re.search(r"\n(SOURCE ISSUES|OPEN MARKERS|#*\s*CHANGES MADE)\b", doc)
    if not m:
        return doc.strip(), ""
    return doc[:m.start()].strip(), doc[m.start():].strip()


def downstream_flag(next_session, topic, mode="new", position="middle",
                    target=None):
    """What the author must fix by hand afterwards. Pure code, no model call.

    Nothing is edited automatically -- the tool reports and the author decides.
    """
    if mode in ("revamp", "repurpose"):
        label = f"unit {target.get('title')}" if target else "the target session"
        out = (
            f"No session was inserted, so the course order is unchanged and no "
            f"other doc's recap or hook is affected.\n\n"
            f"This output is a revised version of {label}. Review it against the "
            f"current doc and replace that file yourself when satisfied -- the "
            f"tool does not overwrite approved material."
        )
        if target and target.get("tr_doc"):
            out += f"\n\nFile it is meant to replace: `{target['tr_doc']}`"
        if next_session:
            out += (
                f"\n\nOne thing to check: if the revision changed what this "
                f"session leaves the learner able to do, the hook of "
                f"**{next_session.get('title')}** may no longer hold.\n"
                f"File: `{next_session.get('tr_doc') or 'no TR doc yet'}`"
            )
        return out

    if not next_session:
        return ("This session goes at the end of the course, so nothing "
                "downstream needs updating.")

    lead = ("This is now the first session of the course, so the session that "
            "used to open it," if position == "first" else
            "The new session now sits before")
    return (
        f"{lead} **{next_session.get('title')}** "
        f"(position {next_session.get('seq') or next_session.get('unit_number')}).\n\n"
        f"That doc was written assuming a different session came before it. Its "
        f"opening recap and its hook are now wrong. Update these sections by hand "
        f"(this tool never edits an approved doc):\n\n"
        f"- Introduction - \"what was learned last session\" must now refer to "
        f"*{topic}*\n"
        f"- Recap table - must now list this session's steps\n"
        f"- The Hook - check its premise still holds now that the learner arrives "
        f"knowing {topic}\n\n"
        f"File: `{next_session.get('tr_doc') or 'no TR doc recorded for it'}`"
    )
