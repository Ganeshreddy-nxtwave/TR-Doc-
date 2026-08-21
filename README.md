# TR Doc Generator

Generates Technical Reference docs for Generative AI course sessions, in your
house style, from a topic and its position in the curriculum.

Standalone Python on OpenRouter. Two front-ends over one engine: a CLI and a
Streamlit web app. No Claude Code needed at runtime.

- Terminal: `python -m tr new`
- Browser: `streamlit run app.py` (see [DEPLOY.md](DEPLOY.md) for hosting)

## Install

```
pip install -r requirements.txt
export OPENROUTER_API_KEY=sk-or-...        # PowerShell: $env:OPENROUTER_API_KEY="sk-or-..."
```

Verify the model slugs in `config.yaml` at <https://openrouter.ai/models> before
the first run. They are not auto-detected; a wrong slug fails on the first call.

## Use

```
# 1. build the curriculum from the status tracker (order + deck URLs)
python -m tr curriculum --tracker "tracker.csv"           # list courses, no output
python -m tr curriculum --tracker "tracker.csv" --course BLANK --rows 26-50 \
       --doc-course "Generative AI" --out curricula/genai-2026.yaml

# 2. distill the house style (once). --from-curriculum ingests decks by URL.
#    NOTE: --curriculum is a top-level flag, so it goes BEFORE the subcommand.
python -m tr --curriculum curricula/genai-2026.yaml style --from-curriculum --dry-run
python -m tr --curriculum curricula/genai-2026.yaml style --from-curriculum --limit 20

# 3. check where the new session lands, before spending any tokens
python -m tr --curriculum curricula/llm-apps.yaml \
       plan --dry-run --topic "Agentic RAG" --after 21

# 4. research + questions, then generate
python -m tr --curriculum curricula/llm-apps.yaml \
       plan --topic "Agentic RAG" --after 21 \
       --learner "knows Python and LangChain basics, non-native English" \
       --produces "working code"
# answer the questions in work/agentic-rag/questions.md
python -m tr write --slug agentic-rag
```

Output lands in `out/<slug>.md` and `out/<slug>-report.md`. **Read the report
before shipping the doc** — it carries the downstream-impact flag, the snippet
verification results, source issues found in your material, and the self-check
failures.

## The web app

`app.py` is three screens over the same engine: set up the job, answer the
questions it must not guess, get the doc and its report. See
[DEPLOY.md](DEPLOY.md) for running it locally and deploying to Streamlit
Community Cloud.

**Code execution is off unless `TR_LOCAL=1`.** Rule 5 works by running the
model's Python to capture genuine output. That is fine on your own machine and
wrong on a shared server, where nobody has reviewed the generated code. The app
defaults to not executing, so a forgotten setting is never the unsafe outcome;
hosted docs carry `[UNVERIFIED]` markers with the command to reproduce each one,
and the report says plainly that no output in that doc is a verified run.

## Sub-topics: telling it what to cover

Optional. Leave it blank and the tool chooses the session's scope itself from the
research, as before. Fill it in — one sub-topic per line in the app, or
`--subtopics "a; b; c"` on the CLI — and it becomes the session's scope.

Treated as a **minimum, not a ceiling**:

- every listed sub-topic must be genuinely taught, not just mentioned
- covered in your order unless a different order teaches better, and a reorder
  must be explained in one line
- the hook is built to lead into the first sub-topic, so the doc has one
  through-line from the opening problem to the last sub-topic
- the flow summary must account for every one
- anything the build genuinely needs but you did not list is added and reported
  under `ADDED BEYOND SCOPE`, one line each with why
- a sub-topic that cannot be taught from the previous session's knowledge is
  flagged `[NEEDS: prerequisite for <sub-topic>]` rather than silently dropped

This is what makes the chain read properly: previous session left the learner
here, these sub-topics move them there, and What's Next hands off to the
following session.

## The three modes

`plan` (aliased as `new`) asks what kind of job this is, because the pedagogy
differs:

| Mode | What it needs | What the prompt enforces |
|------|---------------|--------------------------|
| **new** | a position: first, between, or last | Written from scratch to the seven rules |
| **revamp** | the target session + a change brief | Apply the brief to outline and takeaways; preserve everything it does not touch; keep the Unit ID and position; list every change under `CHANGES MADE` |
| **repurpose** | the target session + a change brief | Same, framed as explicit removals and additions; re-check the through-line afterwards and repair what the edit broke |

Placement changes the pedagogy too:

| Position | Hook | Recap | What's Next |
|----------|------|-------|-------------|
| **first** | From the `HOOK FOUNDATION` you supply — the wizard asks, nothing is inferred | Prerequisites the learner brings, labelled as such | The session that used to open the course |
| **between** | Rule 1 as written: derived from the previous session | The previous session's steps | The following session |
| **last** | Rule 1 as written | The previous session's steps | No next session exists — closes on what the learner can now build, and never invents one |

Revamp and repurpose write to `out/<slug>.md` and **never overwrite the corpus
doc**. The report names the file the output is meant to replace, and confirms
that no session was inserted so no other doc's recap is affected.

## Inputs

| File | What it is | Who writes it |
|------|-----------|---------------|
| `baseline.md` | Everything the learner already knows across all 53 earlier units | Hand-written by you |
| tracker CSV | Session order and deck URLs, per course | Exported from your sheet |
| `curriculum.yaml` | Session order, deck URLs, unit IDs | Generated by `tr curriculum --tracker` |
| `style-guide.md` | How your docs sound: voice, formatting, callouts | Generated by `tr style`, then edited by hand |
| `sources.yaml` | Trusted domains | Hand-edited |
| `corpus/ppts/links.txt` | Slide decks by URL, one per line | Hand-edited (optional) |
| `prompts/tr_doc.md` | The seven rules and the section order | Hand-edited |
| `prompts/modes/*.md` | Per-mode instructions: new, revamp, repurpose | Hand-edited |
| `prompts/positions/*.md` | Per-position instructions: first, middle, last | Hand-edited |

## Design decisions

Recorded here so the reasoning survives, since these were deliberate choices
and not defaults.

**The rules own structure; the style guide owns voice.** The existing 54 docs
predate the seven rules — across all of them, `Recap` appears in 1, `Try It
Yourself` in 5, `What's Next` in 0. So the style guide is explicitly forbidden
from prescribing section order, and `prompts/tr_doc.md` states that the section
order wins where the two disagree. Without this the two inputs fight and the
output is nondeterministic.

**`baseline.md` is a first-class input.** Rule 1 says "assume the learner knows
only the previous session", but in practice they know 53 units across three
courses. The hand-written baseline goes into every generation and into the
self-check, so "did the doc re-teach something they already know" is a question
the checker can actually answer.

**Output depth is calibrated to a reference doc, and the calibration is
tested.** The first generated doc was correct but thin -- 652 lines, a hook that
listed what *might* go wrong, one three-row design-decision table, finished code
shown rather than assembled. `prompts/tr_doc.md` is now calibrated to a
hand-written reference (a 1,027-line AI-agents TR doc): ~13 sections with deep
insides, roughly 900-1,200 lines. The `=== DEPTH ===` block names the nine
patterns that make the difference -- the hook's escalation to a case the old
approach cannot be patched for, a components table mapping concept parts to what
the learner actually types, piece-by-piece assembly stating what breaks without
each piece, post-build property sections, several named scenario runs including a
negative case, and inline design decisions. A test asserts all of it, plus that
the heavier meta-scaffolding of a second reference (verify-flags table, agenda,
checkpoint, coverage ledger) stays banned -- so the prompt cannot drift thin or
bloated unnoticed.

**The writer gets an explicit token budget.** `max_output_tokens: 32000`. Without
it the provider default applies and caps the doc far below a full session; this
was the single largest cause of thin output, independent of the prompt.

**Prompt lives in markdown, not Python.** The seven rules, the structure, the
formatting and language rules are `prompts/tr_doc.md`, injected verbatim. Output
quality is tuned by editing that file. The code's job is to fill its placeholders
with real neighbour content and real research — never to rewrite the rules.

**No retrieval index.** No embeddings, no vector store. The previous and next
session's TR docs go in **verbatim** — the recap table and the hook depend on
exact wording, which retrieved fragments lose. Everything else the tool needs
about house style is distilled once into `style-guide.md`.

**One code path for revamp and repurpose.** Both are "an existing doc plus a
change brief"; only the framing differs. They share `resolve_target`, the same
context plumbing and the same output policy, and differ only in a ~15 line prompt
block. Two near-duplicate prompt files would drift apart within a month.

**Every prompt variation is a file, not a branch.** `prompts/modes/*.md` and
`prompts/positions/*.md` are injected into `prompts/tr_doc.md` through the
existing `fill()` placeholders. Adding a mode or a placement is a new markdown
file, not a code change. An unknown name fails loudly and lists the valid ones,
so a typo can never produce a doc silently missing its instructions for the run.

**Placement is checkable before anything exists.** `plan --dry-run` resolves the
neighbours and stops -- no style guide, no API key, no network needed. It prints
which doc the recap will be built from and which doc you will have to update
afterwards. A wrong position wastes a whole generation run, so it is the cheapest
check in the pipeline and the first one you should make.

**Two-phase run.** `plan` writes `questions.md`; you answer it; `write` reads it.
The things the tool must not guess — unit ID, unit number, final library version,
whether an output is real — become a reviewable artifact instead of a chat
exchange that vanishes. Also means the whole thing works unattended in a script.

**The tracker owns order; the doc headers own identity.** Session sequence and
deck URLs come from the status tracker CSV, because LMS unit numbers collide (two
Generative AI docs both claim unit 33) and skip (they count quizzes and labs).
Unit ID and LMS unit number come from the doc headers, matched to tracker rows by
title. So the ordering key in a generated curriculum is `seq`, and `unit_number`
is metadata that may be null — null means the tool asks rather than guesses.

**Title matching is three signals, and refuses to guess across courses.**
`title_score` takes the best of character edit ratio, whole-title containment
(`Integrating MCP` inside `Integrating MCP Servers in LangChain Agents`), and
content-word set overlap (`Building a Memory Agent` vs `Building an Agent with
Memory` — same words, reordered). The candidate pool is scoped to docs whose
header names that course; if no doc names it, the tool matches **nothing** rather
than borrowing another course's doc, because a silent wrong match is worse than
an honest gap. Matches below 0.85 are printed for manual review.

**Insertion order comes from `seq`, not file order.** `load_curriculum` sorts
before resolving neighbours, so you can append a new session to the end of the
YAML with `seq: "43.5"` and it still resolves to its real position.
Without this an appended session silently looks like the last in the course and
the tool reports no downstream doc to update. Chaining works too — insert after
43.5 and unit 43's "next" becomes 43.5.

**Insertion flags, never edits.** Inserting a session breaks the *next* session's
recap and hook. The report names the exact sections to fix and the file path. The
tool never edits an already-approved doc.

**Trust is ranked, not gated.** `sources.yaml` lists trusted domains. Off-list
sources are still usable but their links must end with `(unofficial source)` in
the doc, so review is one glance. No silent drops, no silent laundering.

**Rule 5 splits by runnability.** Offline-deterministic snippets — Pydantic,
JSON, tokenizers, template rendering — are executed for real and their true
stdout goes in the doc. Anything touching a live model API is written with
`[UNVERIFIED]` and the command to reproduce it, because a single model response
is not a reproducible output and pasting one would quietly violate Rule 6.
Classification is a static text check in `tr/runner.py` (`LIVE_MARKERS`) — free,
deterministic, and wrong only in the safe direction. Add markers to that list if
something slips through.

**Slide decks may be links.** Put local `.pptx` files in `corpus/ppts/`, or list
URLs one per line in `corpus/ppts/links.txt`. A `ppt:` or `tr_doc:` field in
`curriculum.yaml` also accepts a URL. Google Slides and Google Docs share links
are rewritten to their export endpoints, which need no credentials — **but only
if link-sharing is on**. A restricted file returns Google's sign-in page instead
of the deck; that is detected by checking the file signature and reported, rather
than cached as garbage. Org-private decks would need OAuth and the Drive API,
which is not built. Downloads are cached in `.cache/` by URL hash, so a re-run
costs nothing. Connection-level failures retry twice; an HTTP status is a real
answer and is never retried. All 93 tracker decks fetch and parse -- 6,137 slides
in total, verified.

**Snippet execution runs on your machine**, current interpreter, temp cwd, with a
timeout. It is running LLM-generated code, so treat it the way you would treat
running a snippet off a web page. Missing dependencies are reported, not
installed.

## Layout

```
app.py           Streamlit front-end: three screens over the engine
tr/pipeline.py   the engine -- no printing, no stdin, callable from either UI
tr/cli.py        terminal front-end: curriculum | style | new/plan | write
tr/corpus.py     parse .pptx/.md/.docx/.pdf, resolve neighbours,
                 derive curriculum from doc headers, report conflicts
tr/research.py   OpenRouter web search, trust-tag by domain
tr/generate.py   prompt assembly, model calls, downstream flag
tr/runner.py     Rule 5: classify and execute snippets
prompts/         tr_doc.md, style_guide.md, questions.md, self_check.md
baseline.md      student knowledge baseline (hand-written)
curriculum.yaml  session order and unit IDs -- generated, then trusted
curricula/       one generated curriculum per course/cohort
sources.yaml     trusted domains
corpus/ppts/     your .pptx decks, or links.txt listing deck URLs
.cache/          downloaded remote sources, safe to delete
corpus/tr_docs/  your existing TR docs
```

## Test

```
python tests/test_tr.py
```

40 tests. Offline: no API key, no network. Covers snippet classification, real
execution and splicing, position resolution including out-of-order inserts,
doc-header parsing, conflict detection, tracker CSV parsing with forward-filled
merged cells and lost-hyperlink detection, title matching (reorder, containment,
near-miss rejection, cross-course refusal), `.pptx` parsing with speaker notes,
Google share-link rewriting, and domain trust matching.

## Not built

- No auto-patching of downstream docs (flagged only, by choice)
- No cross-course search (add embeddings if terminology consistency across
  courses becomes a real problem)
- No web UI (CLI only)
- No slide generation — the doc is the deliverable

## Known issues in the loaded corpus

Reported by `python -m tr curriculum`, not fixed. Three of these need your
decision before the affected sessions can be used as source material.

1. **Three docs contain the wrong content.** `35-...interview-assistant-part-1`,
   `37-...interview-assistant-part-2` and `47-building-a-game-development-crew`
   are byte-identical to `33-ai-in-the-real-world`,
   `29-building-ai-agents-using-langchain` and
   `45-building-multi-agent-systems-using-crew-ai` respectively. The download
   saved the wrong file under those three names, so those three TR docs are
   effectively missing. Confirmed independently twice: by content hash, and by
   the title matcher leaving exactly these three sessions unmatched in
   `llm-apps.yaml`.
2. **Unit number collision.** In Generative AI, `33-introduction-to-ai-agents`
   and `33-mastering-ai-audio-generation` have different Unit IDs but both claim
   Unit Number 33. One of them is wrong.
3. **AI for Finance has 18 sessions and no TR docs at all.** Every session in
   that course is something this tool would write from scratch. Its 17 decks all
   fetch and parse, so the slides are available as source material.
4. **Two cohorts share the tracker's blank course column.** Rows 1-24 are one
   Generative AI run, rows 26-50 another (`Introduction to Gen AI - 2026` at row
   25 is the divider). Slice them with `--rows`; they are built as
   `curricula/genai-c1.yaml` and `curricula/genai-2026.yaml`.
