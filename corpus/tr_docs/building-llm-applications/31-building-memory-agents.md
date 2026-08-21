# Building Memory Agents

**Course:** Building LLM Applications  
**Topic:** Building AI Agents Using LangChain and Memory Agents  
**Unit ID:** `5a7eda2ea39244baa9a3035df868fad1` | **Unit Number:** 31

---

# Building Memory Agent using Langchain

## Introduction
In the previous session, we built the **SkillMap Agent** that helps to understand skill demand and find job openings.

Agents with memory are AI systems that can store and use past information to make better decisions in the present and future.

**Agent with memory = Large Language Model + Persistent Memory Store**

### Popular Types of Memory
1. **Short-Term Memory**
2. **Long-Term Memory**

### Short-Term Memory
Short-term memory refers to the model’s ability to remember information relevant to the current conversation or session.

* Recent messages
* Results from tool calls
* Task context

### Long-Term Memory
Long-term memory retains information across multiple sessions and interactions.

* User Preferences
* Interaction data
* Learned Behaviors

### Types of Long-Term Memory
Long-term memory can further be divided into three types:

1. **Episodic Memory**
2. **Procedural memory**
3. **Semantic memory**

---

## The Problem: Agent That Forgets
**Testing the SkillMap Agent**

* **User**: "What's the demand for generative ai in the industry and show me related job openings in India"
* **Agent**: *Responds with GenAI demand info and job listings*
* **User**: "Tell me more about the second job you showed"
* **Agent**: "I don't have information about previous jobs. Could you specify which job?"

**Agent forgot the previous conversation!** Each invocation starts fresh with no access to previous conversations.

### Understanding Why Agents Forget
**Current Agent Behaviour**
Each `agent.invoke()` call is completely independent. There’s no connection between calls by default. Every time we call the agent, it is a **NEW** session.

### The Need for Persistence
We need to save the conversation somewhere, so the agent can look back.
Two questions arise:
1. Where do we save it?
2. How does the agent find the right conversation?

**This is where LangGraph helps us!**


### Various Options for persistence include:

* LangGraph Built-in Persistence - Checkpointers
* LangChain - RunnableWithMessageHistory 
* Custom Vector Database Integration
* External Memory Services - Mem0.ai/Zep


### What is LangGraph?
LangGraph is a low-level orchestration framework for building, managing, and deploying long-running, stateful agents.

* Built by LangChain Inc. (creators of LangChain).
* Focuses on state management and memory.
* Can be used independently OR with LangChain.

### LangGraph vs LangChain
* **LangGraph**: Low-level (state, memory, persistence, checkpoints).
* **LangChain**: High-level (create_agent, tools).

LangChain’s `create_agent()` is built on top of LangGraph. This means we can use LangGraph’s memory features directly with our agent.


### Types of Memory in LangGraph
* **Short-Term memory**: Short-term memory enables agents to track multi-turn conversations
* **Long-Term memory**: Long-term memory stores user-specific or application-specific data across conversations


## Implementing Short-term Memory for our Skill Map Agent

* **User**: "Show me GenAI jobs"
* **Agent**: *Here are 5 jobs: Data Scientist, AI Engineer*
* **User**: "Tell me about Job 2"
* **Agent**: *Here’s more about job : AI Engineer*

We want the agent to remember that "AI Engineer" refers to the second item in the previous list. To achieve this, we need something that can save messages automatically.

### Checkpointer
A Checkpointer is a mechanism that automatically saves the conversation state after each message. Each checkpoint contains the complete conversation history up to that point.

### Implementing Checkpointer

`InMemorySaver` is a simple checkpointer implementation that saves conversations in RAM.

* **What does it save?** All messages in the chat.
* **Where does it save?** In RAM (temporary).
* **When is it deleted?** When we refresh the session or stop the program.

<MultiLineNote>
`InMemorySaver` is for development only. For production, use **Persistent Checkpointers** such as:

* SqliteSaver
* PostgresSaver
</MultiLineNote>

### Import and Create Checkpointer Instance
```python
from langgraph.checkpoint.memory import InMemorySaver
checkpointer = InMemorySaver()
```

### Add checkpointer to Agent
```python
agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[skill_demand_tool, search_jobs],
    checkpointer=checkpointer  # ← Add this!
)
```
`checkpointer=checkpointer` tells LangGraph to enable persistence. Without it, the agent won't save any state.

---

## Finding the Right Conversation
Now that we're saving conversations, we need a way to identify them. 

### Thread_id
LangGraph uses the configurable dictionary to pass runtime parameters. The `thread_id` within it tells the checkpointer which conversation thread to use.

**config = {"configurable": {"thread_id": "1"}}**
Think of it like a phone number for your chat:

* **Same thread_id** → Same conversation continues.
* **Different thread_id** → New conversation starts.


### Configuring thread_id
```python
config = {"configurable": {"thread_id": "1"}}
```

### Using thread_id in Agent Invocation
```python
user_query = "What's the demand for generative AI in the industry and show me related job openings in India"

response = agent.invoke({
  "messages": [{"role": "user", "content": user_query}]
}, config=config)

print(response["messages"][-1].content)
```
Using the same `config` (with the same `thread_id`) allows the agent to access previous messages in that conversation.

<details>
<summary>Final Code</summary>

```python
import requests
from google.colab import userdata
from langchain.tools import tool
from langchain_tavily import TavilySearch
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

TAVILY_API_KEY = userdata.get("TAVILY_API_KEY")
RAPIDAPI_KEY = userdata.get("RAPIDAPI_KEY")
GOOGLE_API_KEY = userdata.get("GOOGLE_API_KEY")

skill_demand_tool = TavilySearch(
    max_results=5,
    search_depth="advanced",
    tavily_api_key=TAVILY_API_KEY,
)

@tool
def search_jobs(skill: str, location: str) -> list:
    ""
    Search for jobs requiring a specific skill using the JSearch API.
    ""
    print("\nCalling search_jobs tool")
    print(f"Searching jobs for: {skill} in {location}")
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "jsearch.p.rapidapi.com",
    }
    params = {
        "query": f"{skill} in {location}",
        "page": "1",
        "num_pages": "1",
        "country": "in",
        "employment_types": "INTERN,FULLTIME",
        "job_requirements": "no_experience,under_3_years_experience",
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    jobs = data.get("data", [])
    print(f"Found {len(jobs)} jobs\n")
    return [
        {
            "title": job.get("job_title"),
            "company": job.get("employer_name"),
            "location": job.get("job_city"),
            "apply_link": job.get("job_apply_link"),
        }
        for job in jobs
    ]

SYSTEM_PROMPT = ""
You are a Skill-to-Career Mapping assistant that helps students understand skill demand
and find matching job opportunities.

You have access to these tools:
- skill_demand_tool: Research industry demand, salary insights, and career trends
- search_jobs: Find real job listings based on skills and location

Present results in a clean, readable format with clear sections and spacing.
Include all job details with apply links.
Do not use markdown formatting.
""

model = init_chat_model(
    "google_genai:gemini-2.5-flash",
    api_key=GOOGLE_API_KEY,
)

checkpointer = InMemorySaver()
config = {"configurable": {"thread_id": "1"}}

agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[skill_demand_tool, search_jobs],
    checkpointer=checkpointer,
    debug=True,
)

user_query = (
    "What's the demand for generative AI in the industry "
    "and show me related job openings in India"
)

response = agent.invoke(
    {"messages": [{"role": "user", "content": user_query}]},
    config=config,
)

print(response["messages"][-1].content[0]["text"])

user_query = "Tell me more about the second job you showed"

response = agent.invoke(
    {"messages": [{"role": "user", "content": user_query}]},
    config=config,
)

print(response["messages"][-1].content[0]["text"])

```
</details>
---

## Short Term Memory: Context Overflow
As conversation grows, problems arise:

* Exceeds LLM's context window.
* LLM gets "distracted" by old messages.
* Slower responses, higher costs.

### Context Overflow Strategies

* **Trim Messages**: Remove first few messages & retain last N messages.
* **Delete Messages**: Delete messages from LangGraph state permanently.
* **Summarize Messages**: Summarize earlier messages and replace them with a summary.
* **Custom Strategies**: Message filtering, etc.