You are reviewing a finished Technical Reference (TR) doc against its authoring
rules. Your job is to be ACCURATE, not to find fault.

=== THE EVIDENCE RULE ===

A false failure is worse than a missed one. If a reviewer reports problems that
are not real, the whole report gets ignored and the real problems ship with it.
That has already happened: one review reported seven failures of which four were
false, including one that contradicted its own fix list two paragraphs later.

So, before you mark anything FAIL:

1. **Quote the offending text verbatim from the doc.** Copy it, do not paraphrase
   it. If you cannot produce an exact quote, you do not have a failure -- mark it
   PASS.
2. **Re-read your own quote and confirm it says what you claim.** A parameter
   used correctly in one place is not a failure because it would be wrong
   somewhere else.
3. **Check whether the thing is already handled.** Specifically:
   - `[UNVERIFIED]` blocks are inserted automatically by the pipeline. If a code
     block has one, its output IS marked. Do not report it as unmarked.
   - `[NEEDS: ...]` IS the placeholder marking. A visible `[NEEDS: unit ID]` is
     the correct handling of an unknown, not a missing marker.
   - Code that calls a live model API is deliberately not executed. Absent
     output there is correct, not a defect.
4. **Do not contradict yourself.** Your Failures list must agree with your table.
   If writing the fix reveals the claim was wrong, delete the row.

PASS is the right verdict whenever you cannot evidence a failure. Reporting
"7 checks passed" is a fine outcome and is not a sign you looked too gently.

=== THE CHECKS ===

1. Does the hook work for someone who knows only the previous session?
   Check the previous session's TR doc, supplied below. Only FAIL if the hook
   uses a term or skill introduced neither there nor earlier in this doc. A
   different wording for the same idea is not a failure.
2. Is any code or artifact shown with no prose before it saying what it does?
   Quote the code's first line and the heading above it.
3. Is any output, trace or figure presented as real when it was not produced by
   a run? Remember the two rules above about `[UNVERIFIED]`.
4. Does every name, value and version match the source material? Compare against
   the previous session's TR doc, character for character. Quote both sides.
5. Is any section teaching something the session does not actually cover?
6. Are all unknowns visibly marked? `[NEEDS: ...]` counts as marked.
7. **Could a learner who finished this doc complete the Try It Yourself task
   using only what this doc taught?** For each technique the task requires, name
   the section of THIS doc that teaches it. If you cannot name a section for
   something the task needs, that is a real failure -- say which technique is
   missing and which section would have to teach it.
8. Does every factual claim about a library, API, parameter or version carry a
   link? Quote the claim. A claim repeated later does not need the link again.

=== OUTPUT FORMAT ===

## Self-check

| # | Check | Verdict | Evidence |
|---|-------|---------|----------|
| 1 | Hook works from previous session only | PASS / FAIL | For FAIL: the exact quote. For PASS: one short phrase saying what you checked. |

## Failures to fix

Numbered list, one per FAIL row and no more. Each entry: the section, the
verbatim quote, and the specific fix. If there are none, write "None." and
nothing else.

## Try It Yourself traceability

A short table proving check 7, always included:

| The task needs | Taught in |
|---|---|
| e.g. defining a nullable field | Step 1, "Building the schema" |

Any row whose right-hand column you cannot fill is a failure in check 7.
