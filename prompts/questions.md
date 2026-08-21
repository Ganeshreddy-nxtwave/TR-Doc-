You are preparing to write a Technical Reference (TR) doc for a new course
session. Before writing, you must list the things you MUST NOT GUESS.

Read the supplied context: the course curriculum, the previous session's TR
doc, the next session's TR doc, the house style guide, and the research notes.

Then output a markdown questions file with this exact shape:

# Questions before writing: {{topic}}

Answer inline under each question. Leave blank to accept the stated default.

## Blocking
Questions where a wrong guess would break the doc's structure. For each:

### Q1. <the question>
- Why it matters: <one line>
- My best guess: <your guess, or "none">
- Answer:

## Non-blocking
Same shape, for things that would only change wording or depth.

RULES:
- Ask about unit ID and unit number if the curriculum does not state them for
  this new session. Never invent them.
- Ask which exact library or model version is final if research found more
  than one, or if the version changed recently.
- Ask whether any output, benchmark figure or error trace you plan to show is
  real, and where it came from.
- Ask about anything in the previous session's doc that the new session would
  contradict or supersede.
- Do not ask questions the supplied context already answers. Fewer, sharper
  questions are better than a long list. Aim for at most 6 blocking questions.
