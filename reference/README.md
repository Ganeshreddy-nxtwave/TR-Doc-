# Worked exemplars

TR docs that got the *teaching* right. Every `tr write` run injects these so the
model imitates a real doc rather than following prose rules that describe one.

The prompt tells the writer to take only the teaching moves — how the hook
escalates, when a diagram beats prose, where an analogy goes, how theory and code
interleave — and explicitly NOT to copy the subject, the code, or the section
titles.

## What is here

| File | Why it is an exemplar |
|---|---|
| `building-an-ai-agent-from-scratch.md` | Hook escalates to a question whose answer cannot be pre-written. Concept section carries three tables of theory before any build code. Core mechanism assembled as `Piece 1..6`, each stating what breaks without it. Post-build sections on the mechanism's properties. Scenario runs including a negative case. |

## Where it disagrees with the house rules

This doc has no `What's Next`, no `<MultiLineNote>` callouts, and no
`<a href="..." target="_blank">` links. Those are house requirements, so
`prompts/tr_doc.md` states that STRUCTURE and FORMATTING win over the exemplar on
exactly those three points. Everything else about how it teaches, follow.

## Adding another

Drop a `.md` file in. Keep the folder small — every file is sent on every run.
One strong exemplar beats three mediocre ones. `--no-exemplar` skips them for a
cheap run.
