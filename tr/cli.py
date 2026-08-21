"""tr - Technical Reference doc generator (command line).

  tr curriculum --tracker CSV     derive a curriculum from the status tracker
  tr style                        distill the corpus into style-guide.md (once)
  tr new                          plan a session; asks for whatever is missing
  tr write --slug S               generate the doc from your answers

The generation engine lives in pipeline.py, so app.py can call the same code.
This module is the terminal front-end: prompts, menus and printing.
"""
import argparse
import json
import re
import sys
from pathlib import Path

from . import corpus, generate, pipeline


def slugify(text):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")


class NeedsInput(SystemExit):
    """Raised instead of prompting when --non-interactive is set."""


def ask(label, default=None, allow_blank=False, interactive=True):
    """One line of input. Enter accepts the default."""
    if not interactive:
        if default is not None or allow_blank:
            return default
        raise NeedsInput(f"--non-interactive, but {label!r} was not supplied.")
    suffix = f" [{default}]" if default else ""
    while True:
        got = input(f"{label}{suffix}: ").strip()
        if got:
            return got
        if default is not None:
            return default
        if allow_blank:
            return None
        print("  (required)")


def choose(label, options, interactive=True, default=None):
    """Numbered menu. `options` is a list of (value, display) pairs."""
    if len(options) == 1:
        print(f"{label}: {options[0][1]}  (only option)")
        return options[0][0]
    if not interactive:
        if default is not None:
            return default
        raise NeedsInput(f"--non-interactive, but {label!r} was not supplied.")
    # "[1] 12. Title" -- the bracket is the pick key, the number after it is the
    # session's own position. Keeping them visually distinct avoids "12. 12.".
    print(f"\n{label}:")
    for i, (_, display) in enumerate(options, 1):
        print(f"  [{i}] {display}")
    while True:
        got = input(f"Pick 1-{len(options)}: ").strip()
        if got.isdigit() and 1 <= int(got) <= len(options):
            return options[int(got) - 1][0]
        print("  (enter a number from the list)")


def discover_courses(directory="curricula"):
    """Every curriculum on disk, so the course is a menu not a remembered path."""
    import yaml

    out = []
    for p in sorted(Path(directory).glob("*.yaml")):
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        sessions = data.get("sessions") or []
        out.append((p.as_posix(), data.get("course", p.stem), len(sessions)))
    return out


def describe(session):
    """Human label for a session. Tracker curricula have seq and may have a null
    unit_number, so never print 'unit None'."""
    pos = corpus.order_value(session)
    unit = session.get("unit_number")
    tail = f" [LMS unit {unit}]" if unit else " [no LMS unit yet]"
    return f"{pos}. {session.get('title')}{tail}"


def cmd_style(args):
    cfg = corpus.load_config(args.config)
    if args.from_curriculum:
        _, sessions = corpus.load_curriculum(args.curriculum)
        items = []
        for s in sessions:
            if s.get("ppt"):
                text = corpus.read_pptx(s["ppt"])
                if text:
                    items.append((Path(f"[deck] {s['title']}"), text))
            if s.get("tr_doc"):
                text = corpus.read_text_file(s["tr_doc"])
                if text:
                    items.append((Path(s["tr_doc"]), text))
        print(f"From {args.curriculum}: {len(sessions)} session(s) -> "
              f"{len(items)} source file(s)")
    else:
        items = corpus.collect_corpus(cfg["corpus_ppts"], cfg["corpus_tr_docs"])
    if args.filter:
        items = [(p, t) for p, t in items if args.filter in p.as_posix()]
    if args.limit:
        items = items[: args.limit]
    if not items:
        raise SystemExit(
            f"No material found in {cfg['corpus_ppts']} or {cfg['corpus_tr_docs']}"
            + (f" matching {args.filter!r}" if args.filter else "")
            + ". Drop your .pptx decks and existing TR docs there first."
        )
    print(f"Reading {len(items)} file(s):")
    for p, text in items:
        print(f"  {p}  ({len(text):,} chars)")

    total = sum(len(t) for _, t in items)
    print(f"\n{total:,} chars total, roughly {total // 4:,} tokens in one request.")
    if total // 4 > 120_000:
        print("That is a large single call. If the model rejects it, narrow with "
              "--filter <substring> or --limit N and run again.")
    if args.dry_run:
        print("--dry-run: stopping before the API call.")
        return
    guide = generate.distill_style(generate.client(cfg), cfg["models"]["writer"], items)
    Path(cfg["style_guide"]).write_text(guide, encoding="utf-8")
    print(f"\nWrote {cfg['style_guide']} ({len(guide):,} chars). Read it and edit "
          "anything it got wrong -- every later run depends on this file.")


def curriculum_from_tracker(args, records):
    """Build a curriculum from the status tracker CSV merged with doc headers."""
    rows = corpus.read_tracker(args.tracker)
    print(f"Read {len(rows)} session row(s) from {args.tracker}")

    courses = {}
    for r in rows:
        courses.setdefault(r["course"] or "(blank course column)", []).append(r)
    print("\nCourses in the tracker:")
    print(f"  {'sessions':>8} {'deck URLs':>9} {'lost links':>10}   course")
    for c, rs in courses.items():
        n_url = sum(1 for r in rs if r["ppt"])
        n_lost = sum(1 for r in rs if r.get("ppt_label"))
        print(f"  {len(rs):>8} {n_url:>9} {n_lost:>10}   {c}")

    lost = sum(1 for r in rows if r.get("ppt_label"))
    if lost:
        print(f"\n{lost} PPT cell(s) held a hyperlink whose URL the CSV export "
              "dropped, keeping only the display text. Those decks cannot be "
              "fetched. See 'Recovering deck URLs' in README.md.")

    if not args.course:
        print("\nPick one with --course \"<name>\" (use \"\" for the blank column).")
        print("Slice a cohort out of a shared block with --rows A-B.")
        return

    label = args.course
    rows = [r for r in rows if r["course"] == ("" if label == "BLANK" else label)]
    if not rows:
        raise SystemExit(f"No tracker rows for course {label!r}.")

    # BLANK selects the tracker's empty course column; it is not a course name.
    # Use the real name the docs carry, so the curriculum is not titled "BLANK".
    if label == "BLANK":
        label = args.doc_course or "Unnamed course"

    if args.rows:
        try:
            lo, hi = (int(x) for x in args.rows.split("-", 1))
        except ValueError:
            raise SystemExit("--rows expects A-B, e.g. --rows 26-50")
        rows = [r for r in rows if lo <= r["row"] <= hi]
        print(f"\nSliced to tracker rows {lo}-{hi}: {len(rows)} session(s)")

    dupes = {}
    for r in rows:
        dupes.setdefault(corpus.norm_title(r["title"]), []).append(r["row"])
    repeated = {k: v for k, v in dupes.items() if len(v) > 1}
    if repeated:
        print(f"\n{len(repeated)} REPEATED SESSION NAME(S) -- this block probably "
              "holds more than one cohort. Slice it with --rows:")
        for k, v in list(repeated.items())[:6]:
            print(f"  rows {v}  {k}")

    rows, unmatched = corpus.match_docs(rows, records,
                                        course=args.doc_course or (
                                            None if label == "BLANK" else label))
    matched = [r for r in rows if r["tr_doc"]]
    print(f"\nMatched {len(matched)}/{len(rows)} session(s) to an existing TR doc.")

    weak = [r for r in matched if r["match_score"] < 0.85]
    if weak:
        print(f"\n{len(weak)} LOW-CONFIDENCE MATCH(ES) -- check these by hand:")
        for r in weak:
            print(f"  {r['match_score']}  {r['title'][:46]:<46} -> {r['tr_doc']}")

    no_doc = [r for r in rows if not r["tr_doc"]]
    if no_doc:
        print(f"\n{len(no_doc)} session(s) with NO TR doc (these are what the tool "
              "would write):")
        for r in no_doc:
            print(f"  seq {rows.index(r) + 1:>3}  {r['title'][:56]}"
                  f"{'' if r['ppt'] else '   (and no PPT either)'}")

    if unmatched:
        print(f"\n{len(unmatched)} TR doc(s) NOT in this course's tracker rows:")
        for r in unmatched[:12]:
            print(f"  {r['path']}")

    text = corpus.render_tracker_curriculum(rows, label)
    out = Path(args.out or "curriculum.yaml")
    out.write_text(text, encoding="utf-8")
    print(f"\nWrote {out}: {len(rows)} session(s), "
          f"{sum(1 for r in rows if r['ppt'])} with PPT links.")


def cmd_curriculum(args):
    cfg = corpus.load_config(args.config)
    records = corpus.scan_docs(cfg["corpus_tr_docs"])
    if not records:
        raise SystemExit(f"No .md docs found under {cfg['corpus_tr_docs']}.")

    if args.tracker:
        return curriculum_from_tracker(args, records)

    courses = {}
    for r in records:
        courses.setdefault(r["course"] or "(no course in header)", []).append(r)
    print(f"Scanned {len(records)} doc(s) across {len(courses)} course(s):")
    for c, rs in sorted(courses.items()):
        print(f"  {len(rs):>3}  {c}")

    issues = corpus.curriculum_issues(records)
    if issues:
        print(f"\n{len(issues)} ISSUE(S) -- these are reported, not fixed:\n")
        for i in issues:
            print(f"  * {i}\n")

    if not args.course:
        print("Pick one with --course \"<name>\" to write curriculum.yaml.")
        return
    text = corpus.render_curriculum(records, args.course)
    out = Path(args.out or "curriculum.yaml")
    out.write_text(text, encoding="utf-8")
    n = text.count("- unit_id:")
    print(f"\nWrote {out} with {n} session(s) for {args.course!r}.")


MODES = [
    ("new", "New - a session that does not exist yet"),
    ("revamp", "Revamp - change an existing session's outline and takeaways"),
    ("repurpose", "Repurpose - remove and add parts of an existing session"),
]

POSITIONS = [
    ("between", "In between two existing sessions"),
    ("first", "First session of the course"),
    ("last", "Last session of the course"),
]

# Derived from baseline.md, so the options match cohorts that actually exist.
# Free text still works everywhere; these are the common cases.
LEARNER_PROFILES = [
    "knows Python basics, non-native English",
    "Sem1 Gen AI: uses AI tools and no-code workflows, no Python assumed, "
    "non-native English",
    "Sem2 early: Python basics, Colab, REST APIs with Flask, non-native English",
    "Sem2 mid: builds LLM apps in Python with google-genai and Gradio, "
    "non-native English",
    "Sem2 late: comfortable with LangChain, RAG and agents, non-native English",
    "Sem3: full LLM app stack including evaluation and multi-agent systems, "
    "non-native English",
]

# The first two keep the build sections. The rest replace them with the
# reasoning chain -- see "If the session produces no build" in prompts/tr_doc.md.
PRODUCES = [
    ("working code", "working code - a program the learner builds and runs"),
    ("a working integration",
     "a working integration - wiring an external API or service"),
    ("a design", "a design - no code; problem, options, trade-offs, decision"),
    ("a decision framework",
     "a decision framework - when to choose what, and why"),
    ("an analysis", "an analysis - findings from data or a comparison"),
]


def interview(args):
    """Fill in whatever was not passed as a flag. Returns a plan spec dict.

    Anything already given as a flag is never asked about, so a fully-flagged
    call is non-interactive by construction.
    """
    ia = not args.non_interactive

    topic = args.topic or ask("New session topic", interactive=ia)

    # Course: a menu over curricula/, unless --curriculum was pointed somewhere.
    curriculum = args.curriculum
    if curriculum == "curriculum.yaml":       # the default, i.e. not chosen
        found = discover_courses()
        if found:
            curriculum = choose(
                "Which course",
                [(p, f"{name}  ({n} sessions)  {p}") for p, name, n in found],
                interactive=ia, default=curriculum)

    course, sessions = corpus.load_curriculum(curriculum)

    mode = args.mode or choose("Is this topic", MODES, interactive=ia,
                               default="new")

    spec = {"topic": topic, "curriculum": curriculum, "course": course,
            "sessions": sessions, "mode": mode, "position": "middle",
            "after": None, "at": None, "change_brief": None,
            "hook_foundation": None,
            # Optional scope. Blank means the tool chooses the scope itself.
            "subtopics": args.subtopics or (
                ask("Sub-topics to cover, any order (optional, separate with ';')",
                    interactive=ia and not args.dry_run, allow_blank=True))}
    if spec["subtopics"]:
        spec["subtopics"] = "\n".join(
            f"- {s.strip()}" for s in spec["subtopics"].split(";") if s.strip())

    def session_menu(label):
        return choose(label,
                      [(corpus.order_value(s), describe(s)) for s in sessions],
                      interactive=ia)

    if mode == "new":
        position = args.position or choose("Where does it go", POSITIONS,
                                           interactive=ia, default="between")
        if args.after and not args.position:
            position = "between"
        if position == "between":
            spec["position"] = "middle"
            spec["after"] = args.after or session_menu("Insert it AFTER which session")
        else:
            spec["position"] = position
            if position == "first":
                spec["hook_foundation"] = ask(
                    "This is the first session, so there is no previous one.\n"
                    "  What does the learner arrive already knowing? (a prior "
                    "course, a prerequisite, a real-world problem)",
                    interactive=ia, allow_blank=True)
    else:
        spec["at"] = args.at or session_menu(f"Which session are you {mode}ing")
        spec["change_brief"] = args.change_brief or ask(
            f"What should change? (new outline, changed takeaways, what to "
            f"remove or add)", interactive=ia, allow_blank=True)

    # A dry run only resolves placement, so do not make the author answer
    # questions whose answers are about to be thrown away.
    ask_details = ia and not args.dry_run
    spec["learner"] = args.learner or ask(
        "Learner profile", default="knows Python basics, non-native English",
        interactive=ask_details)
    spec["produces"] = args.produces or ask(
        "This session produces", default="working code", interactive=ask_details)
    return spec


def cmd_plan(args):
    cfg = corpus.load_config(args.config)
    spec = interview(args)
    sessions, course = spec["sessions"], spec["course"]
    mode = spec["mode"]

    target, prev, nxt = pipeline.resolve(
        sessions, mode, position=spec["position"], after=spec["after"],
        at=spec["at"])

    prev_doc = corpus.read_text_file(prev["tr_doc"]) if prev and prev.get("tr_doc") else None
    next_doc = corpus.read_text_file(nxt["tr_doc"]) if nxt and nxt.get("tr_doc") else None
    target_doc = (corpus.read_text_file(target["tr_doc"])
                  if target and target.get("tr_doc") else None)

    print(f"\nCourse:   {course}")
    print(f"Job:      {mode.upper()}"
          + (f" of {describe(target)}" if target else
             f", position {spec['position']}"))
    print("Previous: " + (f"{describe(prev)}"
                          f"{'' if prev_doc else '  (NO TR DOC)'}"
                          if prev else "none (first in the course)"))
    print("Next:     " + (f"{describe(nxt)}"
                          f"{'' if next_doc else '  (NO TR DOC)'}"
                          if nxt else "none (last in the course)"))

    # Placement is checkable before anything else exists -- no style guide, no
    # API key, no network. Check it first, because a wrong position wastes a run.
    if args.dry_run:
        print("\n--dry-run: placement only, no API calls made.")
        if target:
            if target.get("tr_doc"):
                print(f"  revising: {target['tr_doc']}")
                print("  output goes to out/, the current doc is never overwritten")
            else:
                print("  revising: NOTHING -- this session has no TR doc, so there "
                      "is no current version to revise. Use --mode new instead.")
        else:
            span = (f"before {corpus.order_value(nxt)}" if prev is None else
                    f"after {corpus.order_value(prev)}" if nxt is None else
                    f"between {corpus.order_value(prev)} and "
                    f"{corpus.order_value(nxt)}")
            print(f"  the new session sits {span}")
        if prev:
            print(f"  recap and hook built from: {prev.get('tr_doc') or 'the deck '
                  'only -- this session has no TR doc'}")
            if prev.get("ppt"):
                print(f"  previous session's deck: {prev['ppt'][:74]}")
        elif spec.get("hook_foundation"):
            print(f"  hook rests on: {spec['hook_foundation'][:70]}")
        else:
            print("  no previous session and no hook foundation given -- the doc "
                  "will carry [NEEDS: what the learner arrives knowing]")
        if nxt and not target:
            print(f"  doc you must update afterwards: "
                  f"{nxt.get('tr_doc') or 'none (it has no TR doc yet)'}")
        return

    # Fail before spending research tokens, not at `write` time.
    pipeline.check_revisable(mode, target, target_doc, describe)

    style = pipeline.read_style(cfg)
    spec["slug"] = args.slug or slugify(spec["topic"])
    workdir = Path(cfg["work_dir"]) / spec["slug"]
    workdir.mkdir(parents=True, exist_ok=True)

    log = lambda m: print(m)
    notes_md = pipeline.run_research(cfg, args.sources, spec, course, prev, nxt,
                                     log=log)
    (workdir / "research.md").write_text(notes_md, encoding="utf-8")

    ctx = pipeline.build_context(spec, course, target, prev, nxt, describe)
    (workdir / "context.json").write_text(json.dumps(ctx, indent=2),
                                          encoding="utf-8")

    docs = {"prev_doc": prev_doc, "next_doc": next_doc, "target_doc": target_doc}
    qs = pipeline.plan_session(cfg, spec, ctx, docs, notes_md,
                              pipeline.read_baseline(cfg, log), style, log=log)
    (workdir / "questions.md").write_text(qs, encoding="utf-8")

    print(f"\nNext step: answer the questions in {workdir / 'questions.md'},")
    print(f"then run:  python -m tr write --slug {spec['slug']}")


def cmd_write(args):
    cfg = corpus.load_config(args.config)
    workdir = Path(cfg["work_dir"]) / args.slug
    ctx_file = workdir / "context.json"
    if not ctx_file.exists():
        raise SystemExit(f"{ctx_file} not found. Run `tr plan` for this slug first.")
    ctx = json.loads(ctx_file.read_text(encoding="utf-8"))

    answers = (workdir / "questions.md").read_text(encoding="utf-8")
    if re.search(r"^- Answer:\s*$", answers, re.MULTILINE):
        print("Warning: questions.md still has blank Answer: lines. The doc will "
              "carry [NEEDS: ...] markers where they were needed.", file=sys.stderr)

    ctx["prev_doc"] = (corpus.read_text_file(ctx["prev_doc_path"])
                       if ctx.get("prev_doc_path") else None)
    ctx["next_doc"] = (corpus.read_text_file(ctx["next_doc_path"])
                       if ctx.get("next_doc_path") else None)
    # read_pptx resolves local paths and URLs alike, and returns None if neither.
    ctx["prev_ppt"] = (corpus.read_pptx(ctx["prev_ppt_path"])
                       if ctx.get("prev_ppt_path") else None)
    ctx["target_doc"] = (corpus.read_text_file(ctx["target_doc_path"])
                         if ctx.get("target_doc_path") else None)
    pipeline.check_revisable(ctx.get("mode"), ctx.get("target_session"),
                            ctx["target_doc"], describe)

    notes_md = (workdir / "research.md").read_text(encoding="utf-8")
    baseline = pipeline.read_baseline(cfg, print)
    docs = {k: ctx.get(k) for k in
            ("prev_doc", "next_doc", "prev_ppt", "target_doc")}

    result = pipeline.write_session(
        cfg, ctx, docs, answers, baseline, pipeline.read_style(cfg), notes_md,
        execute_snippets=cfg.get("execute_snippets", True),
        log=lambda m: print(m),
    )

    outdir = Path(cfg["out_dir"])
    outdir.mkdir(parents=True, exist_ok=True)
    doc_path = outdir / f"{args.slug}.md"
    doc_path.write_text(result["doc"], encoding="utf-8")
    report_path = outdir / f"{args.slug}-report.md"
    report_path.write_text(result["report"], encoding="utf-8")

    print(f"\nDoc:    {doc_path}")
    print(f"Report: {report_path}   <- read this before you ship the doc")


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="tr", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--curriculum", default="curriculum.yaml")
    ap.add_argument("--sources", default="sources.yaml")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("style", help="distill the corpus into style-guide.md")
    s.add_argument("--from-curriculum", action="store_true",
                   help="read decks and docs listed in the curriculum (needed to "
                        "ingest PPTs by URL) instead of scanning corpus/")
    s.add_argument("--filter", help="only files whose path contains this substring")
    s.add_argument("--limit", type=int, help="only the first N files")
    s.add_argument("--dry-run", action="store_true",
                   help="show what would be sent, make no API call")
    s.set_defaults(fn=cmd_style)

    c = sub.add_parser("curriculum",
                       help="derive curriculum.yaml from the docs' header blocks")
    c.add_argument("--course", help="course name exactly as it appears in the "
                                    "source; use BLANK for the tracker's empty "
                                    "course column")
    c.add_argument("--tracker", help="status tracker CSV: authoritative for "
                                     "session order and PPT links")
    c.add_argument("--rows", help="slice tracker rows A-B, to separate cohorts "
                                  "sharing one course block")
    c.add_argument("--doc-course", help="course name as it appears in the TR doc "
                                        "headers, when it differs from the "
                                        "tracker's (e.g. BLANK -> Generative AI)")
    c.add_argument("--out", help="output path (default curriculum.yaml)")
    c.set_defaults(fn=cmd_curriculum)

    def add_plan_args(q):
        q.add_argument("--topic", help="the session topic (asked for if omitted)")
        q.add_argument("--mode", choices=[m for m, _ in MODES],
                       help="new | revamp | repurpose (asked for if omitted)")
        q.add_argument("--position", choices=["first", "between", "last"],
                       help="where a NEW session goes (asked for if omitted)")
        q.add_argument("--after", help="position the new session goes after, "
                                      "when --position between")
        q.add_argument("--at", help="position of the session being revamped or "
                                    "repurposed")
        q.add_argument("--change-brief", help="what to change, for revamp or "
                                             "repurpose")
        q.add_argument("--subtopics", help="sub-topics this session must cover, "
                                          "separated by ';'. Any order -- the doc "
                                          "sequences them itself. Blank lets the "
                                          "tool choose the scope")
        q.add_argument("--slug")
        q.add_argument("--learner",
                       help="learner profile: level, prior knowledge, language")
        q.add_argument("--produces",
                       help="working code / a design / a decision framework")
        q.add_argument("--non-interactive", action="store_true",
                       help="fail rather than prompt for anything missing")
        q.add_argument("--dry-run", action="store_true",
                       help="resolve placement and stop, no API calls")
        q.set_defaults(fn=cmd_plan)

    add_plan_args(sub.add_parser(
        "plan", help="plan a session: asks what it needs, then researches it"))
    add_plan_args(sub.add_parser(
        "new", help="alias of plan, for starting from a new topic"))

    w = sub.add_parser("write", help="generate the doc from your answered questions")
    w.add_argument("--slug", required=True)
    w.set_defaults(fn=cmd_write)

    args = ap.parse_args(argv)
    args.fn(args)


if __name__ == "__main__":
    main()
