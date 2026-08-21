"""Streamlit front-end for the TR doc generator.

Run locally:   streamlit run app.py
Hosted:        push to GitHub, deploy on Streamlit Community Cloud, put
               OPENROUTER_API_KEY in the app's Secrets.

The generation engine is tr/pipeline.py -- this file only collects input and
shows output. Anything that reads or writes the repo is deliberate and marked.
"""
import json
import os
from pathlib import Path

import streamlit as st

from tr import corpus, pipeline
from tr.cli import describe, discover_courses, slugify

st.set_page_config(page_title="TR Doc Generator", page_icon="📘",
                   layout="wide")

MODES = {
    "new": "New — a session that does not exist yet",
    "revamp": "Revamp — change an existing session's outline and takeaways",
    "repurpose": "Repurpose — remove and add parts of an existing session",
}
POSITIONS = {
    "between": "In between two existing sessions",
    "first": "First session of the course",
    "last": "Last session of the course",
}


# --- environment ----------------------------------------------------------

def running_hosted():
    """True when this is not the author's own machine.

    Streamlit Cloud exposes no official marker, so the decision is explicit:
    set TR_LOCAL=1 to opt in to code execution. Defaulting to "hosted" means a
    forgotten setting is the safe outcome, never the unsafe one.
    """
    return os.environ.get("TR_LOCAL", "").strip() not in ("1", "true", "yes")


def load_api_key():
    """Secrets first (hosted), then the environment (local)."""
    try:
        if "OPENROUTER_API_KEY" in st.secrets:
            os.environ["OPENROUTER_API_KEY"] = st.secrets["OPENROUTER_API_KEY"]
            return True
    except Exception:
        pass                       # no secrets.toml at all, which is fine locally
    return bool(os.environ.get("OPENROUTER_API_KEY"))


@st.cache_data(show_spinner=False)
def cached_courses():
    return discover_courses()


@st.cache_data(show_spinner=False)
def cached_curriculum(path):
    return corpus.load_curriculum(path)


def reset_to(step):
    st.session_state.step = step


def blocking_reason(topic, has_key, target):
    """Whether the generate button is disabled, and why.

    Returns (bool, str). The bool must be a real bool -- Streamlit's `disabled`
    goes into a protobuf field, so `None` from a short-circuiting `and` raises
    TypeError rather than reading as False.
    """
    if not topic:
        return True, "Enter a topic to continue."
    if not has_key:
        return True, "No OPENROUTER_API_KEY, so nothing can be generated."
    if target is not None and not target.get("tr_doc"):
        return True, ("That session has no TR doc, so there is nothing to "
                      "revise. Use mode **new** instead.")
    return False, ""


# --- state ----------------------------------------------------------------

st.session_state.setdefault("step", 1)
st.session_state.setdefault("spec", {})
st.session_state.setdefault("artifacts", {})

hosted = running_hosted()
has_key = load_api_key()

with st.sidebar:
    st.markdown("### Environment")
    st.write("Hosted" if hosted else "Local")
    if has_key:
        st.success("API key found", icon="🔑")
    else:
        st.error("No OPENROUTER_API_KEY", icon="🔑")
        st.caption("Hosted: add it in Settings → Secrets. "
                   "Local: set it in your shell.")

    st.markdown("### Rule 5 — code execution")
    if hosted:
        st.info("**Off.** Generated Python is not executed here, so every code "
                "block is marked `[UNVERIFIED]` with the command to reproduce "
                "it. Run the same session locally to capture real outputs.")
        execute = False
    else:
        execute = st.checkbox(
            "Execute offline snippets for real output", value=True,
            help="Runs model-generated Python in a temp directory to capture "
                 "genuine stdout. Snippets that call a live model API are never "
                 "executed.")
        if not execute:
            st.caption("Off — every block will be marked `[UNVERIFIED]`.")

    if st.session_state.step > 1:
        st.divider()
        if st.button("Start over", use_container_width=True):
            st.session_state.clear()
            st.rerun()

st.title("📘 TR Doc Generator")

# ==========================================================================
# Step 1 -- what are we making
# ==========================================================================
if st.session_state.step == 1:
    st.caption("Step 1 of 3 — what are we making")

    courses = cached_courses()
    if not courses:
        st.error("No curricula found in `curricula/`. Build one first with "
                 "`python -m tr curriculum --tracker <csv> --course <name>`.")
        st.stop()

    # Catch this now, not after the research call has already been paid for.
    style_file = Path(corpus.load_config()["style_guide"])
    if not style_file.exists():
        st.error(f"`{style_file}` is missing. Every doc depends on it, so "
                 "generate it first:\n\n"
                 "```\npython -m tr --curriculum curricula/genai-2026.yaml "
                 "style --from-curriculum --limit 16\n```\n\n"
                 "Then read it and correct anything it got wrong about your "
                 "pedagogy before generating docs.")
        st.stop()

    labels = {p: f"{name}  ·  {n} sessions  ·  {Path(p).name}"
              for p, name, n in courses}
    col_a, col_b = st.columns([3, 2])
    with col_a:
        topic = st.text_input("Session topic",
                              placeholder="e.g. Structured Outputs with Pydantic")
        curriculum = st.selectbox("Course", list(labels),
                                  format_func=lambda p: labels[p])
    with col_b:
        mode = st.radio("Is this topic", list(MODES),
                        format_func=lambda m: MODES[m])

    course, sessions = cached_curriculum(curriculum)
    session_labels = {corpus.order_value(s): describe(s) for s in sessions}

    spec = {"topic": topic, "curriculum": curriculum, "mode": mode,
            "position": "middle", "after": None, "at": None,
            "change_brief": None, "hook_foundation": None}

    st.divider()

    if mode == "new":
        position = st.radio("Where does it go", list(POSITIONS),
                            format_func=lambda p: POSITIONS[p], horizontal=True)
        if position == "between":
            spec["position"] = "middle"
            spec["after"] = st.selectbox(
                "Insert it after", list(session_labels),
                format_func=lambda k: session_labels[k])
        else:
            spec["position"] = position
            if position == "first":
                st.info("There is no previous session, so Rule 1 has nothing to "
                        "derive the hook from. Tell it what the learner arrives "
                        "knowing — a prior course, a prerequisite, or the "
                        "real-world problem the course opens on.")
                spec["hook_foundation"] = st.text_area(
                    "What does the learner arrive already knowing?",
                    placeholder="e.g. They finished Building LLM Applications: "
                                "they can build and deploy an LLM app in Python.")
    else:
        spec["at"] = st.selectbox(
            f"Which session are you {mode}ing", list(session_labels),
            format_func=lambda k: session_labels[k])
        spec["change_brief"] = st.text_area(
            "What should change?",
            placeholder=("Revamp: the new outline and the takeaways you want.\n"
                         "Repurpose: what to remove, what to add."),
            height=120)

    st.divider()
    col_c, col_d = st.columns(2)
    with col_c:
        spec["learner"] = st.text_input(
            "Learner profile", value="knows Python basics, non-native English")
    with col_d:
        spec["produces"] = st.text_input("This session produces",
                                         value="working code")

    # Placement preview: free, no API call, and catches a wrong choice early.
    try:
        target, prev, nxt = pipeline.resolve(
            sessions, mode, position=spec["position"], after=spec["after"],
            at=spec["at"])
    except SystemExit as e:
        st.warning(str(e))
        st.stop()

    with st.container(border=True):
        st.markdown("**Placement**")
        c1, c2, c3 = st.columns(3)
        c1.markdown("Previous  \n" + (describe(prev) if prev
                                      else "_none — first in course_"))
        c2.markdown("This session  \n" + (f"_{mode}_ of {describe(target)}"
                                          if target else f"**{topic or '…'}**"))
        c3.markdown("Next  \n" + (describe(nxt) if nxt
                                  else "_none — last in course_"))
        if prev and not prev.get("tr_doc"):
            st.caption("The previous session has no TR doc, so the recap table "
                       "will be built from its slide deck.")
        if target and not target.get("tr_doc"):
            st.error(f"{describe(target)} has no TR doc, so there is nothing to "
                     f"{mode}. Use mode **new** instead.")

    blocked, why = blocking_reason(topic, has_key, target)
    if st.button("Research & draft questions", type="primary", disabled=blocked):
        spec["slug"] = slugify(topic)
        spec["course"] = course
        st.session_state.spec = spec
        st.session_state.sessions = sessions
        st.session_state.step = 2
        st.rerun()
    if why:
        st.caption(why)

# ==========================================================================
# Step 2 -- research, then the questions it must not guess
# ==========================================================================
elif st.session_state.step == 2:
    st.caption("Step 2 of 3 — answer what it must not guess")
    spec = st.session_state.spec
    sessions = st.session_state.sessions
    cfg = corpus.load_config()

    if "questions" not in st.session_state.artifacts:
        target, prev, nxt = pipeline.resolve(
            sessions, spec["mode"], position=spec["position"],
            after=spec["after"], at=spec["at"])
        docs = pipeline.load_sources(spec, target, prev, nxt)
        pipeline.check_revisable(spec["mode"], target, docs["target_doc"],
                                 describe)
        ctx = pipeline.build_context(spec, spec["course"], target, prev, nxt,
                                    describe)

        with st.status("Working…", expanded=True) as status:
            try:
                style = pipeline.read_style(cfg)
                notes = pipeline.run_research(cfg, "sources.yaml", spec,
                                              spec["course"], prev, nxt,
                                              log=st.write)
                qs = pipeline.plan_session(
                    cfg, spec, ctx, docs, notes,
                    pipeline.read_baseline(cfg, st.write), style, log=st.write)
            except SystemExit as e:
                status.update(label="Stopped", state="error")
                st.error(str(e))
                st.stop()
            except Exception as e:
                status.update(label="Failed", state="error")
                st.error(f"{type(e).__name__}: {e}")
                st.stop()
            status.update(label="Research and questions ready", state="complete")

        st.session_state.artifacts = {"questions": qs, "research": notes,
                                      "ctx": ctx, "docs": docs, "style": style}
        st.rerun()

    art = st.session_state.artifacts
    st.info("Edit the answers inline, the same way you would edit "
            "`questions.md`. Anything left blank becomes a visible "
            "`[NEEDS: …]` marker in the doc rather than a guess.")
    answers = st.text_area("Questions", value=art["questions"], height=420,
                           label_visibility="collapsed")

    with st.expander("Research findings and sources"):
        st.markdown(art["research"])

    col_a, col_b = st.columns([1, 4])
    with col_a:
        if st.button("← Back"):
            st.session_state.artifacts = {}
            reset_to(1)
            st.rerun()
    with col_b:
        if st.button("Generate the doc", type="primary"):
            st.session_state.answers = answers
            st.session_state.step = 3
            st.rerun()

# ==========================================================================
# Step 3 -- the doc and its report
# ==========================================================================
elif st.session_state.step == 3:
    st.caption("Step 3 of 3 — the doc")
    cfg = corpus.load_config()
    art = st.session_state.artifacts
    spec = st.session_state.spec

    if "doc" not in st.session_state:
        with st.status("Generating…", expanded=True) as status:
            try:
                result = pipeline.write_session(
                    cfg, art["ctx"], art["docs"], st.session_state.answers,
                    pipeline.read_baseline(cfg, st.write), art["style"],
                    art["research"], execute_snippets=execute, log=st.write)
            except Exception as e:
                status.update(label="Failed", state="error")
                st.error(f"{type(e).__name__}: {e}")
                st.stop()
            status.update(label="Done", state="complete")
        st.session_state.doc = result["doc"]
        st.session_state.report = result["report"]
        st.rerun()

    slug = spec["slug"]
    st.success(f"Generated: **{spec['topic']}**")

    c1, c2 = st.columns(2)
    c1.download_button("⬇ Download the doc", st.session_state.doc,
                       file_name=f"{slug}.md", mime="text/markdown",
                       use_container_width=True, type="primary")
    c2.download_button("⬇ Download the report", st.session_state.report,
                       file_name=f"{slug}-report.md", mime="text/markdown",
                       use_container_width=True)

    st.warning("Read the report before shipping the doc. It carries the "
               "downstream-impact flag, the snippet verification results, any "
               "source inconsistencies found in your material, and the "
               "self-check failures.", icon="⚠")

    tab_doc, tab_report, tab_raw = st.tabs(["Doc (rendered)", "Report",
                                            "Doc (markdown)"])
    with tab_doc:
        st.markdown(st.session_state.doc, unsafe_allow_html=True)
    with tab_report:
        st.markdown(st.session_state.report)
    with tab_raw:
        st.code(st.session_state.doc, language="markdown")

    if not hosted:
        st.divider()
        if st.button("Save to out/ on this machine"):
            outdir = Path(cfg["out_dir"])
            outdir.mkdir(parents=True, exist_ok=True)
            (outdir / f"{slug}.md").write_text(st.session_state.doc,
                                               encoding="utf-8")
            (outdir / f"{slug}-report.md").write_text(st.session_state.report,
                                                      encoding="utf-8")
            st.success(f"Written to {outdir / (slug + '.md')}")
