# House Style Guide for Technical Reference Documents

## Hook patterns

**Read this section carefully: the existing docs do NOT hook the way new docs must.**

Here is how the existing docs actually open:
- "In the previous unit, we learned about **prompt engineering** and how to create clear prompts that help AI give better and more accurate answers. In this unit, we will focus on **AI workflows**, which are automated steps that use AI to complete tasks like creating content, analyzing data, and executing tasks automatically without needing human involvement."
- "In the previous unit, we built an AI-Powered Social Media Content Creator & Publisher that automated article listing, summarization, and posting using n8n. In this unit, we'll focus on building our own AI News Summarizer — a personal assistant that fetches news from RSS feeds, summarizes it, and delivers a daily email update."
- "In this unit, we will move beyond the basics of prompting and learn how to guide AI more effectively. We'll explore key prompting techniques such as Zero-shot, One-shot, Few-shot, and Chain-of-Thought, understand the limitations of large language models, and see practical ready-to-use prompts."

Their shared structure is: "In the previous unit… In this unit we will focus on
**X**, which is…" — a recap, then a definition of the new concept.

**That structure is superseded. Do not copy it.** It announces the concept and
defines it up front, which Rule 1 forbids. These docs were written before the
current authoring rules.

What to take from these openings:
- the sentence rhythm — short, plain, concrete
- the vocabulary and reading level
- the habit of naming the previous session's concrete achievement, not an
  abstraction ("we built an AI-Powered Social Media Content Creator", not "we
  explored automation concepts")
- bolding a term the first time it carries weight

What to do instead of their structure: open from what the learner can already
do, put one realistic problem in front of it that their current approach cannot
handle, let them see it fail, and name the new concept only after that. The hook
must reduce to a single question they cannot answer with what they know, and that
question goes in the doc as a callout.

Note the rhetorical-question habit under "Callout style" below — that IS worth
keeping, and it is the closest thing in the existing material to a real hook.

## Recap tables
Real recap table from the material:
```
| Prompting Technique | When it is Best                                                                                                                               |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Zero-shot prompting**   |  The task is straightforward. <br>  The AI likely has seen similar examples during training. <br>  You need a quick response.                    |
| **One-shot prompting**    |  You need a specific format. <br>  The pattern is simple but needs an example.                                                                    |
| **Few-shot prompting**    |  The task involves a more complex pattern. <br>  You need consistent formatting across multiple outputs. <br>  The task requires specialized or domain-specific knowledge. |
| **Chain-of-Thought**    |  Breaks complex problems into smaller, logical steps.<br>  Best for tasks requiring multi-step thinking and careful explanations.                                                                   |
```

Column names used: "Prompting Technique" and "When it is Best". Level of detail: concise bullet points within cells, present tense throughout.

## Section rhythm
Sections typically run 3-8 sentences. Recap tables appear after explaining multiple related concepts. Code/prompt examples appear immediately after their conceptual introduction. Each technique is introduced with a brief definition followed by a `<details>` block containing an example.

## Design-decision sections
Real alternatives table (from slide deck):
```
- ###Manual Process
    Involves reading articles, writing posts, creating different versions for various platforms, and manually posting them.
    
**Read Article Manually** →  **Write LinkedIn Post** →  **Create Instagram Post** →  **Create Twitter Version** → **Post on All Platforms**
    
    Time Taken: **30-45** minutes per article.

- ###AI Workflow Process
    Involves adding a link to an article in a Google Sheet, which then triggers the workflow to create content suitable for multiple platforms and post it.
    
  **Add Article to Sheet** →  **Auto-generate Content** → **Post Everywhere Simultaneously** →  **Send Confirmations**
    
    Time Taken: Less than **2** minutes of human effort.
```

Choice is justified through time comparison and process complexity difference.

## Sentence and vocabulary rules
Sentences average 8-15 words. Contractions are rare; prefer the full form.

Actors are named explicitly and consistently: "the developer", "the system",
"the AI", "the model", "the workflow", "the user". Never blur them — say who
does what.

**On "we":** the existing docs use "we" freely ("we will focus", "we built",
"we'll explore"). That is the house voice for narrating a build the reader is
following along with, and it is fine to keep. But do not use "we" to hide which
actor is acting — "we send the request" is wrong when the point is that *the
system* sends it. When the actor matters, name the actor.

Never uses "basically", "simply put", or casual filler.

## Formatting conventions
- `<details>` for all code examples and lengthy configurations
- `<MultiLineNote>` for important reminders
- `<MultiLineWarning>` for problems and their solutions, structured as "Problem" then "Solution"
- Backticks for inline code, tool names, and file paths
- Links formatted as: `<a href="URL" target="_blank">Display Text</a>`
- Tables using markdown pipe syntax with left-aligned columns

Real example:
```html
<MultiLineWarning text="Solution">
Instead of spending half an hour browsing multiple websites, imagine receiving a perfectly summarized email at 10 AM with only the most relevant AI news.
</MultiLineWarning>
```

## Callout style
Hook questions are phrased as rhetorical questions without expecting answers, formatted as plain text or within warning blocks:
- "Have you ever spent too much time posting on social media about your learning progress/edu/career updates?"
- "What if we want technology news along with AI news?"

## Try It Yourself style
**No real example was found in the material read for this guide** — only 5 of 54
existing docs have a Try It Yourself section at all, so there is no established
house pattern to copy. Treat the guidance below as a starting point, not as
observed practice, and replace this section once a Try It Yourself you like
exists.

The closest existing equivalents are:
- lists of RSS feed URLs to explore
- configuration steps with specific values to enter
- test checklists with verification points

Difficulty: intermediate, assuming the session's own material and nothing beyond
it. One concrete extension task the learner can actually complete with what the
session taught, then a small table of further ideas.

## Anti-patterns observed
- Never uses first-person singular ("I")
- Never includes personal anecdotes or opinions
- Avoids exclamation marks
- Does not use emoji or decorative elements
- No hand-holding imperatives in explanatory prose ("Remember that...", "Note
  that..."). Instructions inside build steps and Try It Yourself tasks ARE
  imperative and should be — "Create the file", "Run the workflow"
- Avoids meta-commentary about the document itself

## What NOT to report
Section order and required sections are determined by separate authoring rules. This guide focuses on the writing style within sections, not their sequence or mandatory inclusion.