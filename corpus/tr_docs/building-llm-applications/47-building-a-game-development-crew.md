# Building Multi Agent Systems Using Crew AI

**Course:** Building LLM Applications  
**Topic:** Building Multi Agent Systems and LLM Evaluation  
**Unit ID:** `3650b1d35288426581d45d68b97755c8` | **Unit Number:** 45

---

# Introduction

In our previous session, we learned about integrating MCP Servers in LangChain Agents — integrating MCP in LangChain, using MultiServerMCPClient, Tavily MCP Server, and retrieving tools from MCP using `get_tools()`.
Now in this unit, we will understand Multi-Agent Systems, and learn how to build multi-agent systems using CrewAI and the core components of Crew AI.

## AI Agent

An AI agent is a system that can operate independently to achieve a specific goal without constant human intervention.

## Beyond Single Agents

Many challenges can be solved with a "Single agent, multi-tool" approach, where one agent is given access to a variety of tools and knowledge sources.

### Example

User asks: "Research latest iPhone and create a comparison doc"

**Single Agent Process:**

1.  Search the web for iPhone info
2.  Read multiple articles
3.  Organize information
4.  Create document
5.  Format it nicely

(All done by ONE agent)

### Challenges of Single-Agent Systems

As tasks become more complex, a single agent might face significant challenges:

*   **Tool Overload** — Managing too many tools can make the Agent harder to make clear decisions. 
*   **Contextual Limitations** — LLMs struggle with performance when context grows.
*   **Specialization Deficiency** — A single agent cannot master diverse tasks.


# Introduction to Multi-Agent Systems

### What is a Multi-Agent System?

A Multi-Agent System is a team of AI agents with specialized roles working together to solve complex tasks efficiently.

### Team of AI Specialists

Multi-Agent Systems are like having a team of AI specialists, where:

*   Each agent has <b>a specific role and expertise</b>
*   Agents can <b>communicate</b> with each other
*   They <b>collaborate</b> to solve complex problems
*   They can <b>share information</b> and <b>delegate tasks</b>
*   Finally, they produce a single output

### Example - Making a Movie

*    **Director** — Plans the overall vision
*    **Actors** — Perform the scenes
*    **Cinematographer** — Handles camera work
*    **Music Composer** — Creates background score
*    **Editor** — Puts everything together

Each person is an expert in their role, and they work together to create the final movie!


### Example - Planning a Wedding

Imagine you're planning a wedding. You need:

*   Someone to handle <b>decorations</b> and make everything beautiful
*   Another person to manage the <b>food</b> and catering
*   Someone to <b>coordinate with guests</b> and handle RSVPs
*   Another to handle <b>entertainment</b> and music

Each person has their own expertise and responsibilities, but they all work together toward the same goal: creating an amazing celebration. This is exactly how Multi-Agent AI Systems work!

### How It Works

Just like each person in a team has a unique role but everyone works toward one goal, a Multi-Agent AI system also works in a similar manner. 

Have you worked in a team where different strengths of different people made the result better than one person doing everything?

### Real World Applications - Trading Systems

Trading systems use multiple agents to monitor markets, analyze trends, execute trades, and manage risk, enabling faster and smarter trading than single-agent systems.

*   **Monitoring Agent** — Collects real-time and historical market data
*   **Strategy Agent** — Analyzes and decides trading actions
*   **Execution Agent** — Places trades efficiently
*   **Risk Management Agent** — Ensures safe and controlled trading

### Real World Applications - Vehicle Systems

Autonomous vehicles use specialized agents for perception, planning, traffic, and safety, working together to navigate complex situations safely.

*   **Perception & Control Agent** — Senses & understands the vehicle's environment and controls the vehicle
*   **Planning Agent** — Plans the vehicle's route
*   **Safety Agent** — Monitors the system for safety (speed limit, etc.)

### Key Characteristics of Multi-Agent Systems

*   **Collaboration** — Agents interact and share information to tackle complex challenges
*   **Autonomy** — Each agent operates independently, making its own decisions
*   **Specialization** — Agents are designed for specific tasks, enhancing efficiency
*   **Scalability** — New agents can be added to the system easily as needs grow

# Building Multi Agent Systems

## Frameworks

There are multiple frameworks that allow us to build multi-agent systems:


*   **<a href="https://www.crewai.com" target="_blank">CrewAI</a>** — Team-based AI agents working together
*   **<a href="https://microsoft.github.io/autogen" target="_blank">AutoGen</a>** — AI agents that talk to each other
*   **<a href="https://github.com/openai/swarm" target="_blank">OpenAI Swarm</a>** — Graph-based multi-step agent workflows
*   **<a href="https://www.langchain.com" target="_blank">LangChain</a>** — Building LLM-powered applications

## Using CrewAI

**CrewAI** is an <b>open-source Python framework</b> that allows us to build, <b>production-ready</b> and collaborative <b>AI agent teams</b> to tackle complex tasks.


## Core Components of CrewAI

CrewAI has three core components:

1.  **Agents**
2.  **Tasks**
3.  **Crew**

### 1. Agents

In CrewAI, an agent is an AI specialist with:

*   **A role** (what they do)
*   **A goal** (what they aim to achieve)
*   **A backstory** (their expertise and personality)
*   **Tools** (capabilities they can use)

Each AI Agent in the Crew has a specific role capable of carrying out multiple role-related Tasks. Agents are equipped with Tools that facilitate them completing the jobs.

** Example - Research Agent**

*   <b>Role:</b> Senior Research Analyst
*   <b>Goal:</b> Find accurate, up-to-date information
*   <b>Backstory:</b> Expert researcher skilled at gathering insights
*   <b>Tools:</b> Web search

**Example - Content Writer Agent**

*   <b>Role:</b> Creative content writer
*   <b>Goal:</b> Write engaging blog posts
*   <b>Backstory:</b> Expert writer with 10 years of experience
*   <b>Tools:</b> Web search, document creation



** Agents are workers in Multi Agent System**


Think of agents as the workers in the system:

*   Each agent is autonomous and specializes in one task
*   Works independently but shares information with other agents
*   Sometimes, relies on others' outputs to do their job better
*   Can also delegate tasks to other agents as and when required

### 2. Tasks

Tasks are specific jobs we want our agents to complete. Each task should have:

*   Clear description of what needs to be done
*   Which agent should handle it
*   Expected output format

#### Example

| | Task 1 | Task 2 |
|---|---|---|
| <b>Task</b> | Research latest AI trends | Use the research report to craft a compelling blog |
| <b>Assigned to</b> | Research Agent | Content Writer Agent |
| <b>Expected Output</b> | Summary report with 5 key trends | A well-written blog post |

### 3. Crew

The crew is your complete team — all agents working together with a defined process:

*   <b>Sequential</b> — Agents work one after another
*   <b>Hierarchical</b>  — One agent manages others
*   <b>Parallel</b> — Agents work simultaneously

**CrewAI Allows Us To…**

*   Create multiple AI agents with different roles
*   Define how they work together
*   Assign them specific tasks
*   Coordinate their collaboration automatically

** Installing CrewAI**

```bash
!pip install -U crewai
```

**Multi Model**

While building multi-agent systems, think of yourself as a manager/leader:

*   What is the Goal?
*   What kind of people would I need to hire to get this done?
*   What is the Process?