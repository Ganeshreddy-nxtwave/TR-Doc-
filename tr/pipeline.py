"""The generation engine, with no front-end in it.

`cli.py` and `app.py` both call these. Nothing here prints, reads stdin, or
knows what a terminal is -- progress goes to an optional `log` callback so the
CLI can print it and a web app can show it in a status box.
"""
from pathlib import Path

from . import corpus, generate, research, runner


def _noop(_msg):
    pass


def resolve(sessions, mode, position=None, after=None, at=None):
    """Neighbours for a job. Returns (target, prev, nxt); target is None unless
    this is a revamp or repurpose."""
    if mode in ("revamp", "repurpose"):
        return corpus.resolve_target(sessions, at)
    prev, nxt = corpus.resolve_placement(
        sessions,
        position=(None if position in (None, "middle", "between") else position),
        after=after,
    )
    return None, prev, nxt


def load_sources(spec, target, prev, nxt):
    """Read every document this job needs. Returns a dict of text blobs."""
    return {
        "target_doc": (corpus.read_text_file(target["tr_doc"])
                       if target and target.get("tr_doc") else None),
        "prev_doc": (corpus.read_text_file(prev["tr_doc"])
                     if prev and prev.get("tr_doc") else None),
        "next_doc": (corpus.read_text_file(nxt["tr_doc"])
                     if nxt and nxt.get("tr_doc") else None),
        "prev_ppt": (corpus.read_pptx(prev["ppt"])
                     if prev and prev.get("ppt") else None),
    }


def build_context(spec, course, target, prev, nxt, describe):
    """The reproducible record of a job, written to context.json.

    `describe` renders a session label; passed in so this module does not own
    presentation.
    """
    return {
        "course": course,
        "topic": spec["topic"],
        "slug": spec["slug"],
        "mode": spec["mode"],
        "position": spec.get("position") or "middle",
        "after": spec.get("after"),
        "at": spec.get("at"),
        "change_brief": spec.get("change_brief"),
        "subtopics": spec.get("subtopics"),
        "hook_foundation": spec.get("hook_foundation"),
        "prev_title": describe(prev) if prev else "",
        "next_title": describe(nxt) if nxt else "",
        "target_title": describe(target) if target else "",
        "prev_doc_path": prev.get("tr_doc") if prev else None,
        "next_doc_path": nxt.get("tr_doc") if nxt else None,
        "prev_ppt_path": prev.get("ppt") if prev else None,
        "target_doc_path": target.get("tr_doc") if target else None,
        "next_session": nxt,
        "target_session": target,
        "learner_profile": spec.get("learner"),
        "session_produces": spec.get("produces"),
    }


def check_revisable(mode, target, target_doc, describe):
    """Refuse a revamp with nothing to revise, before any tokens are spent."""
    if mode not in ("revamp", "repurpose") or target_doc:
        return
    where = (f" ({target['tr_doc']} could not be read)."
             if target and target.get("tr_doc")
             else " (none recorded in the curriculum).")
    raise SystemExit(
        f"Mode is {mode}, but {describe(target)} has no TR doc to revise{where}"
        "\nUse mode 'new' to write it from scratch."
    )


def run_research(cfg, sources_path, spec, course, prev, nxt, log=_noop):
    """Web search, trust-tagged. Returns the rendered markdown notes."""
    cl = generate.client(cfg)
    log("Researching...")
    notes, urls = research.research(
        cl, cfg["models"]["research"], spec["topic"], course,
        (prev["title"] if prev
         else (spec.get("hook_foundation") or "nothing in this course yet")),
        nxt["title"] if nxt else None,
        corpus.trusted_domains(sources_path),
    )
    n_trusted = sum(1 for _, ok in urls if ok)
    log(f"  {len(urls)} source(s): {n_trusted} trusted, "
        f"{len(urls) - n_trusted} unvetted")
    return research.render_notes(spec["topic"], notes, urls)


def plan_session(cfg, spec, ctx, docs, notes_md, baseline, style, log=_noop):
    """Phase one: produce the questions file. Returns its markdown."""
    cl = generate.client(cfg)
    log("Writing questions...")
    return generate.build_questions(cl, cfg["models"]["writer"], {
        **ctx, **docs, "style": style, "research": notes_md,
        "baseline": baseline,
    })


def write_session(cfg, ctx, docs, answers, baseline, style, notes_md,
                  execute_snippets=True, log=_noop):
    """Phase two: generate, verify snippets, self-check.

    Returns {"doc", "report", "results"}. Writes nothing to disk -- the caller
    decides where output goes, because a web app has no repo to write into.
    """
    cl = generate.client(cfg)
    full = {**ctx, **docs, "style": style, "research": notes_md,
            "baseline": baseline,
            "max_output_tokens": cfg.get("max_output_tokens")}

    log("Generating doc...")
    raw = generate.write_doc(cl, cfg["models"]["writer"], full, answers)
    doc, trailing = generate.split_trailing_blocks(raw)

    log("Verifying snippets (Rule 5)..." if execute_snippets
        else "Marking snippets unverified (execution off here)...")
    doc, results = runner.verify(doc, cfg.get("run_timeout_seconds", 30),
                                 execute=execute_snippets)
    summary = runner.summarise(results)
    log(summary)

    log("Self-checking...")
    check = generate.self_check(cl, cfg["models"]["checker"], doc,
                                docs.get("prev_doc"), notes_md, baseline)

    report = "\n\n".join([
        f"# Report: {ctx['topic']}",
        "## Downstream impact",
        generate.downstream_flag(ctx.get("next_session"), ctx["topic"],
                                 mode=ctx.get("mode") or "new",
                                 position=ctx.get("position") or "middle",
                                 target=ctx.get("target_session")),
        "## Snippet verification",
        summary if execute_snippets else
        summary + "\n\nCode execution was OFF for this run, so no output in this "
                  "doc is a verified run. Generate the same session locally with "
                  "execution on, or paste your own outputs during review.",
        "## From the writer",
        trailing or "Nothing reported.",
        check,
    ])
    return {"doc": doc, "report": report, "results": results}


def read_baseline(cfg, log=_noop):
    path = Path(cfg.get("baseline", "baseline.md"))
    if not path.exists():
        log(f"Warning: {path} not found. Rule 1 will only see the previous "
            "session, not the full course history.")
        return None
    return path.read_text(encoding="utf-8")


def read_style(cfg):
    path = Path(cfg["style_guide"])
    if not path.exists():
        raise SystemExit(f"{path} not found. Run the style step first.")
    return path.read_text(encoding="utf-8")
