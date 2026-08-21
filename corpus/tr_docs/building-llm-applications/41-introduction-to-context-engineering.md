# Introduction to Context Engineering

**Course:** Building LLM Applications  
**Topic:** Introduction to Context Engineering and MCP  
**Unit ID:** `6f09a1a77d484bb3adaf4456188d5df3` | **Unit Number:** 41

---

# Introduction

In the previous unit, we focused on RAG Agent and Adding agent capabilities to the Docuchat and we built powerful AI applications using function calling, agents, and RAG systems. Now in this unit, we will understand Context Engineering, exploring its core techniques, common failures and fixes, and how it differs from Prompt Engineering.


### Challenges

As we built more complex applications, you might have noticed a pattern:


*   **Agents** sometimes **forget important information** mid-conversation
*   **Performance degrades** as conversations get longer
*   Relevant **information gets** "**lost**" in long context windows
*   **Costs increase** with larger prompts

### Traditional Approach vs Reality

**Traditional Approach:** Focus on crafting the perfect prompt with the right words and instructions.

**Reality:** Modern AI applications need more than good prompts — they need intelligent information management.

##Evolution of Prompt Engineering (Context Engineering)

### Introduction To Context Engineering

Context engineering is the art and science of filling the LLM's context window with just the right information, in the right format, at the right time to accomplish a task.

### Why It Matters

While the term "Context Engineering" is new, the idea isn't. Context engineering helps us solve a key challenge in AI: managing what information flows into and out of AI systems.

### Analogy

Just like a computer needs the right data loaded in RAM to run programs well, your AI needs the right context to perform tasks effectively.

*   CPU → LLM
*   RAM (Limited) → Context Window (Limited)
*   OS -> Context Engineering

### The Shift In Approach

Instead of writing perfect prompts, we build systems that automatically gather and organize information for the model. The system arranges everything so the AI can use it effectively:

*   Past conversations
*   User details
*   Data Sources (RAG)
*   Available tools

### Components of Context Engineering

*   System Instructions
*   Conversation History/Memory
*   Retrieved Knowledge
*   Tool Descriptions
*   Current State
*   User Prompt

<MultiLineNote>
Context Engineering brings together RAG, State/History, Memory, Structured Outputs, and Prompt Engineering.
</MultiLineNote>
### Set Up Context: Claude Projects/Custom GPT
<a href="https://claude.ai" target="_blank">Claude</a>
*   Upload your semester timetable and exam schedule
*   Add your current course materials and lecture notes
*   Include previous assignment grades and feedback
*   Upload syllabus and weightage details for each course

### Enhanced System Instructions

**System Instructions:**

```
You are an academic study assistant for engineering students. You have access to: - Student's current semester subjects and exam schedule - Current course materials - Grades and assignment feedback - Syllabus with weightage
```

**Files**
<a href="https://nkb-backend-ccbp-media-static.s3-ap-south-1.amazonaws.com/ccbp_prod/media/content_loading/uploads/cc1bad21-242a-48fa-942f-3d29c9460361_Academic%20Files.zip" target="_blank">Academic Files</a>

<br>

**Student question:** 

```
What should I focus on for my upcoming mid-semester exams?
```

The system provides an enhanced response based on all the uploaded context.

## Context vs Prompt Engineering

| | Prompt Engineering | Context Engineering |
|---|---|---|
| Focus | Focuses on how you ask the question | Focuses on everything the model sees before responding |
| Scope | The words, tone, and formatting of your input | Includes prompts, system instructions, retrieved documents, memory, tools, and state |
| Example | "Summarize this in 3 bullet points" | Required for complex, multi-step applications and AI agents |

### When to Use Context Engineering

*   Building AI agents or applications
*   Tasks requiring memory across conversations
*   Systems that need to access external tools or databases
*   Complex, multi-step workflows
*   Production applications

### When to Use Prompt Engineering

*   Simple chatbot conversations
*   One-shot Q&A tasks
*   Text summarization or translation
*   Quick factual queries

---

## Common Context Failures and Fixes

### Failure 1: Context Poisoning

**What happens:** The AI saves incorrect information and keeps using it in future responses.

**Example:** One piece of bad data spreads and affects all future decisions.

**Fixes:**

*   Check if information is accurate before saving
*   Only allow trusted sources to write to memory
*   Keep questionable information separate until confirmed

### Failure 2: Context Distraction

**What happens:** Too much information makes the model lose focus on what matters.

**Fixes:**

*   Summarize old conversations instead of keeping everything
*   Pull only the relevant parts, not entire documents
*   Delete outdated or completed information
*   Keep only what's needed for the current task

### Failure 3: Context Confusion

**What happens:** The AI gets confused when it receives too many tools or unclear instructions about what to do.

**Fixes:**

*   Write clear, specific tool descriptions (not vague ones)
*   Show examples of when to use each tool
*   Set clear rules for which tool handles what
*   Use structured formats so the model knows what to expect

### Failure 4: Context Clash

**What happens:** Contradictory information from different sources creates inconsistent behavior.

**Fixes:**

*   Set priority order (which source to trust)
*   Add rules for handling conflicts automatically
*   Remove old information that contradicts new facts
*   Keep one single source of truth for each type of data

---

## Core Context Engineering Techniques

### Technique 1: Writing Context

Saving information outside the context window for later use.

**The Problem and Solution**

<b>Problem:</b>Complex multi-step tasks overload the context window with too much information.

<b>Solution:</b>Use a "scratchpad" — external storage where the AI saves notes, plans, and intermediate results outside the main context window.

** Implementation Methods**

*   File writes (simple text files or JSON)
*   Database inserts (vector databases, SQL databases)
*   Structured memory (LangGraph state, message queues)
*   Long-term memory systems (LangGraph state)

** Benefits**

1.  <b>Prevents overload</b> — Stays within token limits
2.  <b>Remembers across sessions</b> — Information persists between conversations
3.  <b>Keeps AI focused</b> — Main context stays clean and relevant

** Example: Claude Code's Scratchpad**

When working on a large codebase, Claude Code uses a "think" tool as a scratchpad:

```json
{
  "name": "think",
  "thought": "User wants to refactor the login module. Let me consider the current structure, identify pain points, and plan the approach before making changes..."
}
```

Notes are saved outside the main conversation, preventing it from being lost as the context fills up with code.

<MultiLineWarning text="Research Result">

Anthropic found the "think" tool improved performance by 54% on complex customer service tasks.

</MultiLineWarning>

### Technique 2: Selecting Context

Retrieving exactly the right information when needed. Rather than giving the model everything, pull in information dynamically based on the current task.

**Methods**

<b>Retrieval Augmented Generation (RAG):</b>

*   Use semantic search to find relevant documents
*   Hybrid search combining keyword + semantic matching
*   Return only relevant sections, not entire documents

<b>Tool-Based Selection:</b>

*   Model calls specific tools to fetch needed data
*   Tools return structured, filtered information
*   Example: Instead of loading entire database, query for specific records

<b>Contextual Retrieval:</b>

*   Fetch information based on current state/task
*   Use conversation context to refine what's retrieved
*   Prioritize recent and relevant info over comprehensive

### Technique 3: Compressing Context

Reducing context size while preserving important information. Reliable on longer tasks, but hard to get right.

**The Problem and Solution**

<b>Problem:</b>

*   Beyond large number of tokens, models start repeating old actions instead of thinking fresh
*   They may "forget" instructions from the beginning
*   Costs increase dramatically

<b>Solution:</b>Periodically summarize older content, keeping recent messages intact.

- Summarization
- Filtering
- Abstraction


### Technique 4: Isolating Context

Splitting work across specialized agents with focused context. Instead of one agent juggling everything, distribute work, if possible.

**Methods**

- Multi-Agent Decomposition
- Focused Context Per Agent
- Context Passing

---

## The Quality Over Quantity Principle

<b>More context ≠ Better performance.</b><br>


**Context rot:** As input context grows, LLM performance drops in unpredictable ways.

*   Longer context = higher cost AND often lower quality
*   Performance drop depends on model and task — there is no single safe limit for number of tokens
*   A focused 300-token context can outperform an unfocused 100,000+ token context

<a href="https://research.trychroma.com/context-rot" target="_blank">https://research.trychroma.com/context-rot</a>

## The Key Insight

> "Context engineering is effectively the #1 job of engineers building AI agents"
> — Cognition (Devin AI)