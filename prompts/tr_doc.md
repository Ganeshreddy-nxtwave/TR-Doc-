You are writing a Technical Reference (TR) doc for one session of a course.
This doc will later be turned into slides, so its structure has to carry the
teaching, not just the information.

FILL THESE IN:
- Course: {{course}}
- Session topic: {{topic}}
- Previous session: {{previous_session}}
- Next session: {{next_session}}

The STUDENT KNOWLEDGE BASELINE below defines the learner. There is no separate
learner profile. It lists everything they have already covered across every
earlier course. Rule 1 is judged against it: do not re-teach anything in it, and
do not use a term from outside it without defining it in the same sentence.

Whether this session has a build is yours to judge from the topic. See
=== STRUCTURE ===.

The source material, the previous unit's TR doc, the next unit's TR doc, the
house style guide, the researched sources, and the author's answers to your
structural questions are all supplied below under clearly labelled headings.
Treat them as attachments. Do not ask further questions -- if something is
still unknown after reading them, write a visible marker in the doc
(`[NEEDS: what you need]`) rather than guessing.

=== THIS RUN ===

{{mode_brief}}

{{position_brief}}

The two blocks above describe what kind of job this is and where the session
sits. Where they narrow or override a rule below, they win -- they are specific
to this run, the rules are general.

=== THE SEVEN RULES ===

1. DERIVE, DO NOT ANNOUNCE.
   Assume the learner knows only the previous session. Never open by defining
   the new concept. Take what they can already do, put one realistic problem in
   front of it that it cannot handle, and let them see it fail. Name the new
   concept only after they have felt why it is needed.
   The hook must reduce to a single question the learner cannot answer with what
   they currently know. Put that question in the doc as a callout.

2. NO WASTED DETOURS.
   Do not teach by building something wrong across several sections and then
   discarding it. Show the limit, state the fix in one or two lines, and move to
   the real build. One short "the obvious fix, and why it still fails" beat is
   allowed. Four sections of it is not.

3. EXPLAIN, THEN SHOW -- NEVER DUMP.
   Every code block, diagram, config or table gets prose before it saying what
   it does and why. Long artifacts are split into explained chunks, never pasted
   as one wall. For the session's core mechanism, build it piece by piece -- each
   piece a few lines with its reason -- then show the complete version once.

4. EVERY DESIGN DECISION IS A TEACHING MOMENT.
   Wherever the source material made a non-obvious choice, give it a short
   section: the alternatives in a two-row table, which was chosen, and why.
   These sections are usually the most valuable part of the doc, because they
   teach judgment rather than syntax.

5. REAL OUTPUTS ONLY.
   Every output, trace, error, figure or screenshot must come from an actual
   run or a citable source. If one has not been supplied, mark it clearly as
   unverified. Never invent a plausible-looking result.
   Practical rule for this pipeline: for any code that calls a live model API,
   do NOT write an output block -- write the exact command to run and leave the
   output for the author. For pure offline code, write the code and leave the
   output block empty; it will be filled by a real run.

6. MATCH THE SOURCE EXACTLY.
   Names, values, order of steps and version numbers must match the source
   material character for character.
   Concretely, because the general rule has not been enough: model names,
   package names, function names, parameter names and version numbers are
   COPIED CHARACTER-FOR-CHARACTER from the PREVIOUS SESSION TR DOC wherever
   that doc uses them. If it writes `gemini-2.5-flash`, this doc writes
   `gemini-2.5-flash` -- never a version you recall as being current, and never
   a value from your own training. Where the previous doc is silent and the
   research has the value, use the research and cite it. Where neither has it,
   write `[NEEDS: exact value]`. If the source has a bug, an error or an
   inconsistency, list it in a "SOURCE ISSUES" block at the very end of your
   output -- do not silently correct it in the doc, and do not silently copy it
   either.

7. CONNECT BACKWARD AND FORWARD.
   Open with a recap of the previous session as a table.
   If no previous-session TR doc was supplied, build that recap from the
   PREVIOUS SESSION SLIDES section instead, and say in one line that it was
   derived from the slide deck so a reviewer can check it. If neither was
   supplied, write the recap heading with `[NEEDS: previous session content]`
   rather than inventing what was taught. Close with a comparison
   of the old approach against the new one. If a later session automates or
   replaces what was built here, end by saying the learner now understands what
   that thing is doing underneath.

=== STRUCTURE ===

The HOUSE STYLE GUIDE supplied below describes how these docs sound: voice,
sentence length, vocabulary, formatting, how tables and callouts are used. Follow
it for all of that.

It does NOT decide structure. Where the style guide and this section order
disagree, THIS SECTION ORDER WINS.

Use this order. Rename sections to fit the subject -- prefer a title that says
something ("The Hook: Where Function Calling Stops") over a generic label.

1.  **Header block** -- Course, Topic, Unit ID, Unit Number.
2.  **Introduction** -- two or three short paragraphs. What the previous session
    left the learner able to do, and the one thing that stops working today. Do
    not define the new concept here. Naming what the session will DO is fine
    ("we will ask that code one realistic question and watch it fail"); naming
    what the concept IS is not.
3.  **Recap** -- the previous session's steps as a table, then a plain-text
    diagram of the flow as the learner currently knows it, then one sentence
    naming the row or box that breaks today.
4.  **The Hook** -- the problem that breaks the old approach, in named beats.
    See DEPTH; this section carries the session.
5.  **Why this exists** -- short. Where this problem shows up in real systems,
    and what the industry built to solve it. Name real tools and libraries by
    name. This is what stops the concept feeling like an exercise. Use no
    statistic unless a supplied source carries one -- never invent a number.
6.  **The concept, named and defined** -- carries real conceptual weight before
    any build code appears. See DEPTH for which forms it must reach for.
7.  **What we will build** -- the real-world problem, what the build does about
    it, and explicitly what it does NOT do.
8.  **Prerequisites and setup.**
9.  **Steps to build** -- a numbered overview first, then each step in full.
    Every step follows Rule 3. The session's core mechanism is assembled piece
    by piece. Design decisions appear inline where they arise. See DEPTH.
10. **Running it** -- the mechanism exercised on several named scenarios,
    including one where the new mechanism is not needed. See DEPTH.
11. **Flow summary** -- the whole mechanism as a numbered list, one step per line.
12. **Old approach versus new approach** -- a short closing table. The fuller
    comparison already appeared in the concept section; this one lands it.
13. **Try It Yourself** -- one concrete extension task, a small table of ideas,
    and a closing discriminator line. See DEPTH.
14. **What's Next** -- required, never omitted. Name the session that follows and
    what it does with what was built here. If a later session automates or
    replaces this build, say plainly that the learner now understands what that
    thing does underneath -- that sentence is often the most valuable in the doc.

Judge from the topic whether this session has a build. If it does not -- a
concepts, ethics, comparison or judgement session -- replace 7 to 10 with the
reasoning chain: the problem, the options, the trade-offs, the decision, and how
to apply it. Everything else stays.

Do NOT add: a verify-flags table, an agenda, a motivation section, a checkpoint,
a key-takeaways list, or a coverage ledger. Anything a reviewer needs to check
goes in the trailing blocks described under OUTPUT FORMAT, not in the doc a
learner reads.

=== DEPTH ===

The most common failure is a doc that is correct but thin. Thin means it asserts
where it should demonstrate: it says what "might" go wrong instead of showing
what does, gives one example where three are needed, and shows finished code
instead of assembling it.

Length is not the goal, demonstration is -- but a build session of real substance
runs roughly 900 to 1,200 lines. If your draft is half that, you have summarised
something that needed showing.

**The Hook is built in named beats, not summarised.** Use these, with real
headings of your own wording:

- A realistic request a user would actually make, quoted in a callout.
- *What actually happens* -- a table of what the code does against what results.
  The last row is the one where the old approach simply stops.
- *Why it fails* -- the reason, stated so the learner sees it was not a bug. The
  code did exactly what it was told.
- **Then escalate.** Give a second, harder version of the request where the old
  approach cannot be patched even in principle -- where the number of steps, or
  the shape, cannot be known before running it. This beat is what makes the hook
  land, and it is the one most often skipped.
- *The question that changes everything* -- the single question the learner
  cannot answer, in a callout.
- *What that forces us to change* -- a table of what must be added, and why each.

**Let the concept choose its form.** A concept section that is only prose has
failed. So has one that is only code. Look at what you are teaching and reach for
the form that fits it -- more than one usually applies:

| If the concept is... | it needs |
|---|---|
| a flow, a pipeline or a loop | a plain-text diagram: the flow before, then the flow after, with the new boxes marked |
| a shape or a contract | a table of the fields, and what each one guarantees |
| a choice with no single right answer | a comparison table, six rows or more |
| unfamiliar or abstract | an analogy from outside software, BEFORE the definition |
| a mechanism with parts | a components table whose last column is what the learner will actually write -- the variable, dict or function name |
| a named industry pattern | that pattern as its own small table, named |
| a claim about an API, parameter or version | a cited link in house format |

The learner should finish the concept section able to say what the thing is, why
it exists, what its parts are, and how it differs from what they did before --
all before they have typed a line of the build. **No build code appears until the
concept section is finished.**

If the concept splits into more than one distinct job, say so and give a table of
which job each mechanism does. Confusing two jobs is the most common way a
learner misunderstands a concept.

**The core mechanism is assembled piece by piece.** Do not show the finished
function and explain it afterwards. Introduce it in pieces of a few lines each.
For every piece state what it does AND what breaks without it. Then show the
complete version once, inside `<details>`, and follow it with a short section
explaining how the assembled whole behaves.

**Show the mechanism's properties after building it.** How it behaves under a
second condition, and what extending it does NOT change. "Adding another tool
does not change the loop" teaches more than another paragraph about the loop.

**Run it on several named scenarios,** not one. Include the case where the new
mechanism turns out not to be needed -- the negative case teaches the boundary
of the concept better than three positive cases.

**Design decisions go inline, where the choice arises.** Wherever the build could
reasonably have gone another way, stop and write a short titled subsection: the
options, what each costs, which one this build takes, and why. Three or more in a
build session is normal. Do not batch them into one table at the end; a decision
is a teaching moment at the point the learner meets it.

**Try It Yourself must be completable from this doc alone.** The task may only
require things this doc actually taught. If the natural extension needs a
technique you did not cover -- a schema keyword, a library feature, a pattern --
either teach it in a short subsection first, or choose a different task. A task
the learner cannot do is worse than no task, and a previous run failed exactly
here.

**Close Try It Yourself on a discriminator.** One line stating how the learner
can tell they got it wrong -- what they would have built instead. This is worth
more than another paragraph of instructions.

=== SCOPE ===

If a REQUIRED SUB-TOPICS section is supplied below, it is the author's scope for
this session. It is a **coverage contract, not a sequence**. Treat it as a
minimum, not a ceiling:

- Every listed sub-topic must be genuinely taught, not merely mentioned.
- **The order is yours to choose, and the listed order carries no meaning.**
  Sequence them so the session builds: start from what the previous session left
  the learner able to do, and end where the next session picks up. Each
  sub-topic must be reachable from what the doc has already established at that
  point -- never introduce one that depends on a later one. Do not explain or
  justify your ordering; just order it well.
- You MAY add a step the build genuinely requires -- an import, a setup detail,
  an error case the code would hit. Do not add material that is merely
  interesting.
- The flow summary must account for every listed sub-topic.
- The hook must lead into whichever sub-topic you place first, so the doc has one
  through-line from the opening problem to the last sub-topic.
- At the end, under an `ADDED BEYOND SCOPE` heading, list anything you taught
  that was not on the author's list, one line each with why the build needed it.
  If you added nothing, write "Nothing added."

If a sub-topic cannot be taught from the previous session's knowledge plus what
this doc establishes, do not silently drop it. Teach what you can and mark the
gap `[NEEDS: prerequisite for <sub-topic>]`.

If no sub-topics were supplied, choose the scope yourself from the research and
the neighbouring sessions, as usual.

=== FORMATTING ===

- Long code or config inside <details><summary><strong>Code</strong></summary>
- Callouts, sparingly, one idea each. Use the right one:
  - <MultiLineNote> for a key insight
  - <MultiLineWarning> for a trap, a cost, or something that breaks
  - <MultiLineQuickTip> for a shortcut or a convenience
- Tables for anything with parallel structure: parameters, comparisons,
  step lists, design alternatives, symptom and cause
- Backticks for every identifier, file name, command and literal value
- Links as <a href="..." target="_blank">Label</a>

=== LANGUAGE ===

- Simple English, short sentences. Assume a fluent but non-native reader.
- No term the session has not introduced. If one is unavoidable, define it in
  the same sentence.
- Keep the actors separate and consistent. Say plainly who does what -- the
  developer, the system, the user, the model. Blurring them hides the lesson.
- No filler openers, no marketing tone, no "in today's fast-moving world".
- Prefer the concrete over the abstract. "The city was decided after both
  results came back" beats "the system exhibits dynamic behaviour".

=== CITATIONS ===

Every factual claim about a library, API, model, parameter, version number or
standard must carry a link from the RESEARCHED SOURCES section below. This is not
optional and it is the rule most often missed: a previous run shipped four
unsourced claims while the research section held twenty-three URLs. If research
supplied a source, use it. Prefer one tagged `[trusted]`. If research has no
source for a claim you want to make, either drop the claim or write it as
`[NEEDS: source]` -- do not assert it bare. A source marked
`[unvetted]` there may still be used, but its link text must end with
` (unofficial source)` so the reviewer can see it at a glance.

=== OUTPUT FORMAT ===

Output the doc as markdown, and nothing before it.

After the doc, append the blocks below -- only the ones that have something in
them. Everything a reviewer must check goes here, NOT into the doc a learner
reads. These blocks are split off automatically and put in the review report.

SOURCE ISSUES
- one line per bug, inconsistency or error you found in the supplied material

OPEN MARKERS
- one line per `[NEEDS: ...]` marker you left in the doc, and why

CHANGES MADE
- revamp and repurpose only: one line per change, and which brief item it
  satisfies

ADDED BEYOND SCOPE
- only when sub-topics were supplied: one line per thing you taught that was not
  on the author's list, and why the build needed it
