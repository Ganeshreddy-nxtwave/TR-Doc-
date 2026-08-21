# Building AI Agents Using LangChain

**Course:** Building LLM Applications  
**Topic:** Building AI Agents Using LangChain and Memory Agents  
**Unit ID:** `4d21beadef254119b53124a7ac37e308` | **Unit Number:** 29

---

# Introduction

In the previous units, we covered RAG applications and LangChain fundamentals. In this unit, we will learn how to build AI Agents that can autonomously perform tasks by using multiple tools. We'll build a practical **SkillMap Agent** that helps users understand skill demand in the industry and find matching job opportunities.

## What is an AI Agent?

An AI agent is a system that can operate independently to achieve a specific goal without constant human intervention.

### AI Agents Core Components

- **AI Model** (like GPT-5 or Claude): The reasoning engine that makes decisions
- **Tools** (search engines, databases, APIs): External capabilities the agent can use
- **Memory**: Ability to remember context across interactions

---

## Building SkillMap Agent

### The Problem

After learning a skill like Generative AI, common questions arise:

- What is the demand for Generative AI in the industry?
- Which roles require this skill?
- What jobs are available in India?

### The Current Approach

The typical approach is to search manually across multiple sources, getting scattered information from different articles, forums, and job portals. This is time-consuming and often gives incomplete results.

### The Solution

What if you could simply ask:

> "What's the demand for Generative AI skills in the industry? Show me related job openings in India"

And get current market insights, real job openings, and easy-to-apply links all in one response?

This is exactly what our SkillMap Agent will do.

---

###Popular Frameworks for LLM Applications

- <b>LangChain</b>
- LlamaIndex
- Haystack
- Semantic Kernel
- CrewAI
<br> many more...

**LangChain**

It is a open source framework with a pre-built agent architecture and integrations for any model or tool — so you can build agents that adapt as fast as the ecosystem evolves

## SkillMap Agent Core Components


| Component | Purpose |
|-----------|---------|
| Google Gemini | AI reasoning and decision-making |
| Tavily Search | Getting skill demand information |
| JSearch (RapidAPI) | Getting live job links from LinkedIn, Indeed, Glassdoor |
| LangChain | Framework to orchestrate the agent |

---

## Steps to Build the SkillMap Agent

1. Creating the Agent
2. Creating the Skill Demand Search Tool
3. Creating the Job Search Tool
4. Defining System Prompt and Configuring Agent
5. Executing the Agent

---

## Step 1: Creating Agent using LangChain


LangChain provides a method called `create_agent` that lets us create an agent.

### create_agent() - Syntax

```python
agent = create_agent(
  model = model,
  tools = [//list of tools],
  system_prompt = system_prompt,
)
```

** create_agent**

The `create_agent` function creates an agent that calls tools in a loop until a stopping condition is met. The agent runs until the model emits a final output.

### Install LangChain

```python
!pip install langchain
```

```python
from langchain.agents import create_agent

agent = create_agent(
  model = model,
  tools = [//list of tools],
  system_prompt = system_prompt,
)
```
### Defining the Model

Models are the reasoning engine of agents. The model handles:

- The agent's decision-making process
- Determining which tools to call
- How to interpret results
- When to provide a final answer

### Initializing the Model

#### Install Google GenAI Package

```python
!pip install -U langchain-google-genai
```

```python
from langchain.chat_models import init_chat_model
from google.colab import userdata

google_api_key = userdata.get('GOOGLE_API_KEY')
model = init_chat_model(
    "google_genai:gemini-2.5-flash", 
    api_key=google_api_key
)
```

###Configuring the Model

```python
from langchain.agents import create_agent

agent = create_agent(
  model = model,  #The language model instance
  tools = [//list of tools],
  system_prompt = system_prompt,
)

```



---

## Step 2: Creating the Skill Demand Search Tool

### What Our Agent Needs

To provide useful career guidance, our agent needs to fetch real-time market insights like:

- Industry Demand
- Salary Trends
- Career Growth Opportunities

To retrieve this real-time market information, we need a search tool.

### LangChain Core Components
**Tools**

Tools are components that agents call to perform actions. They extend model capabilities by letting them interact with the world through well-defined inputs and outputs.

LangChain offers an extensive ecosystem with 1000+ tool integrations with different platforms.

###LangChain Tool Integrations

LangChain , Python Offers an extensive ecosystem with 1000+ tool integrations with different platforms

### Built-in Tool: Tavily Search

Tavily Search is a search engine built specifically for AI agents (LLMs) delivering real-time, accurate, and factual results at speed.

To find real-time market insights, we'll use Tavily Search.

### Install Tavily Package

```python
!pip install langchain-tavily
```

### Instantiate Tavily Search

- <a href="https://app.tavily.com/home" target="_blank">Tavily API Key</a>

```python
from langchain_tavily import TavilySearch
from google.colab import userdata

tavily_api_key = userdata.get('TAVILY_API_KEY')

skill_demand_tool = TavilySearch(
    max_results=5,
    search_depth="advanced",
    tavily_api_key=tavily_api_key
)
```

### Tavily Search Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| max_results | int | Maximum number of search results | 5 |
| search_depth | str | "basic" or "advanced" | "basic" |
| topic | str | "general", "news", or "finance" | "general" |

### Invocation Arguments

The Tavily search tool accepts the following argument during invocation:

- **query (required)** -> A natural language search query

### Testing the Skill Demand Tool

```python
result = skill_demand_tool.invoke({"query": "generative ai skills demand 2025"})
print(result)
```

---

## Step 3: Creating the Job Search Tool

### What We Need Next

We can now fetch skill demand and salary insights using Tavily Search. But that's only half the picture.

To make this truly useful, we also need to show actual job openings where this skill is required with direct apply links.

### Can Tavily Help Here?

| What We Need | Can Tavily Do It? |
|--------------|-------------------|
| Search skill demand trends | Yes |
| Get salary insights | Yes |
| Find actual job listings with apply links | No |
| Filter jobs by experience level (fresher/intern) | No |
| Get jobs from LinkedIn, Indeed, Glassdoor | No |

### Solution: Integrate with JSearch API

When built-in tools don't meet specific needs, we create Custom Tools.

To fetch live job listings, we'll integrate with RapidAPI's JSearch which gives us access to jobs from LinkedIn, Indeed, Glassdoor, and other major platforms.

### Understanding JSearch API

JSearch allows us to seamlessly access most up-to-date job postings and provides:

- Job titles and descriptions
- Company information
- Location details
- Application links
- Employment types

###Making HTTP Requests

Before creating our tool, let's understand what data the JSearch API returns

###Understanding JSearch Response

- <a href="https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch/playground/endpoint_1a4de4d7-7abd-4ec2-a897-57a0fc5ad496" target="_blank">RapidAPI Key</a>

```python
import requests

rapidapi_key = userdata.get('RAPIDAPI_KEY')

url = "https://jsearch.p.rapidapi.com/search"
headers = {
  "x-rapidapi-key": rapidapi_key,
  "x-rapidapi-host": "jsearch.p.rapidapi.com"
}
querystring = {
  "query": "Generative AI in India",
  "page": "1",
  "num_pages": "1"
}

response = requests.get(url, headers=headers, params=query_string)
print(response.json())

```

###Understanding the API Parameters


| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| query | String | Free-form job search query | "software developer in India" |
| country | String | ISO country code | "in" for India |
| employment_types | String | Comma-separated employment types | "INTERN, FULLTIME" |
| job requirements | String | Experience level filters | "no experience,under 3 years experience" |
| page | Number | Page to return (each page includes up to 10 results) | 1 |

###Built-in Tools

Tavily is a built-in tool in LangChain for web search, but for fetching live job listings from JSearch, we need     to create a custom tool


### Building a Custom Tool

LangChain provides many built-in tools, but for specific requirements like fetching live job listings, a ready-made tool might not exist. In such cases, LangChain lets us integrate our own custom tools.

The simplest way to create a Custom tool is with the `@tool` decorator. By default, the function's docstring becomes the tool's description that helps the model understand when to use it.

###Understanding Tool Syntax


```python
@tool
def function_name(parameter: str) -> str:
    ""Short description of what this tool does.""
    return f"Processed: {parameter}"
```

- **Tool decorator (`@tool`)**: Registers the function as a LangChain tool
- **Type annotations**: Define the input schema and expected output type for the LLM
- **Docstring**: Describes the tool's purpose to help the LLM decide when to use it

### Import and Configure the Tool

```python
import requests
from langchain.tools import tool

@tool
def search_jobs(skill: str, location: str) -> list:
```

- Converts `search_jobs` into a tool the agent can call
- Agent will pass job skill and location as string inputs
- Returns a list of matching job results

### Define the Tool Description

```python
import requests
from langchain.tools import tool

@tool
def search_jobs(skill: str, location: str) -> list:
    ""Search for jobs requiring a specific skill using JSearch API from RapidAPI.""
```

Helps the agent understand this tool searches jobs based on skill and location.

### Set Up API Credentials and Endpoint

```python
import requests
from langchain.tools import tool

@tool
def search_jobs(skill: str, location: str) -> list:
    ""Search for jobs requiring a specific skill using JSearch API from RapidAPI.""
    print(f"\nCalling search_jobs tool")
    print(f"Searching jobs for: {skill} in {location}")

    rapidapi_key = userdata.get('RAPIDAPI_KEY')

    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-key": rapidapi_key,
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }
```

### Build Query Parameters

```python
@tool
def search_jobs(skill: str, location: str) -> list:
    ""Search for jobs requiring a specific skill using JSearch API from RapidAPI.""
    print(f"\nCalling search_jobs tool")
    print(f"Searching jobs for: {skill} in {location}")

    rapidapi_key = userdata.get('RAPIDAPI_KEY')

    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-key": rapidapi_key,
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }
    querystring = {
        "query": f"{skill} in {location}",
        "page": "1",
        "country": "in",
        "employment_types": "INTERN,FULLTIME",
        "job_requirements": "no_experience,under_3_years_experience"
    }
```

### Make the API Call

```python
@tool
def search_jobs(skill: str, location: str) -> list:
    ""Search for jobs requiring a specific skill using JSearch API from RapidAPI.""
    print(f"\nCalling search_jobs tool")
    print(f"Searching jobs for: {skill} in {location}")

    rapidapi_key = userdata.get('RAPIDAPI_KEY')

    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-key": rapidapi_key,
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }
    querystring = {
        "query": f"{skill} in {location}",
        "page": "1",
        "country": "in",
        "employment_types": "INTERN,FULLTIME",
        "job_requirements": "no_experience,under_3_years_experience"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

```

### Extract Key Information

```python
@tool
def search_jobs(skill: str, location: str) -> list:
    ""Search for jobs requiring a specific skill using JSearch API from RapidAPI.""
    print(f"\nCalling search_jobs tool")
    print(f"Searching jobs for: {skill} in {location}")

    rapidapi_key = userdata.get('RAPIDAPI_KEY')

    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-key": rapidapi_key,
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }
    querystring = {
        "query": f"{skill} in {location}",
        "page": "1",
        "country": "in",
        "employment_types": "INTERN,FULLTIME",
        "job_requirements": "no_experience,under_3_years_experience"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    jobs = data.get("data", [])
    print(f"Found {len(jobs)} jobs\n")

    result = []
    for job in jobs:
        result.append({
            "title": job.get("job_title"),
            "company": job.get("employer_name"),
            "location": job.get("job_city"),
            "apply_link": job.get("job_apply_link")
        })
    return result
```

The `.get()` method retrieves data, returning an empty list if "data" doesn't exist.

---


###Creating the Job Search Tool (complete code)


```python
import requests
from langchain.tools import tool
from google.colab import userdata

@tool
def search_jobs(skill: str, location: str) -> list:
    ""Search for jobs requiring a specific skill using JSearch API from RapidAPI.""
    print(f"\nCalling search_jobs tool")
    print(f"Searching jobs for: {skill} in {location}")

    rapidapi_key = userdata.get('RAPIDAPI_KEY')

    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-key": rapidapi_key,
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }
    querystring = {
        "query": f"{skill} in {location}",
        "page": "1",
        "country": "in",
        "employment_types": "INTERN,FULLTIME",
        "job_requirements": "no_experience,under_3_years_experience"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    jobs = data.get("data", [])
    print(f"Found {len(jobs)} jobs\n")

    result = []
    for job in jobs:
        result.append({
            "title": job.get("job_title"),
            "company": job.get("employer_name"),
            "location": job.get("job_city"),
            "apply_link": job.get("job_apply_link")
        })
    return result
```

---

## Step 4: Defining System Prompt and Configuring Agent

### What We Have So Far

- `skill_demand_tool` (TavilySearch): Fetches market insights
- `search_jobs`: Fetches job listings

### What We Need Now

We have both tools ready. Now we need to tell the agent how to use these tools and what role it should play. This is done through a **System Prompt**.

We also need a language model that will act as the brain, deciding which tool to call and when.

### Define System Prompt

```python
system_prompt = ""You are a Skill-to-Career Mapping assistant that helps students understand skill demand and find matching job opportunities.

You have access to these tools:
- skill_demand_tool: Search for industry demand, salary insights, and career trends
- search_jobs: Find actual job listings requiring specific skills

Help the student by researching the skill they ask about and finding relevant opportunities.

Present results in a clean, readable format with clear sections and proper spacing. Include all job details with apply links. Don't use markdown format.""
```

### Configuring System Prompt and Tools


```python
from langchain.agents import create_agent

agent = create_agent(
    model=model,
    tools=[skill_demand_tool, search_jobs],
    system_prompt=system_prompt
)
```

###Removing Tool Invocations

```python
from langchain_tavily import TavilySearch
from google.colab import userdata

tavily_api_key = userdata.get('TAVILY_API_KEY')

skill_demand_tool = TavilySearch(
  max_results=5,
  search_depth="advanced",
  tavily_api_key=tavily_api_key
)

#Removing Tool Invocations
#result = skill_demand_tool.invoke({"query": "generative ai skills demand 2025"})
#print(result)

```
---

## Step 5: Executing the Agent

###create_agent Parameters

To execute our agent, we use the `invoke` method which triggers the complete workflow.

All agents include a sequence of messages in their state. To invoke the agent, pass a new message with the user's query.


### Run the Agent

All agents include a sequence of messages in their state -> To invoke the agent, pass a new message with the user's query


### Invoke the Agent

```python
user_query = "What's the demand for generative ai in the industry and show me related job openings in India"

response = agent.invoke({
    "messages": [{"role": "user", "content": user_query}]
})
```

### Getting the Response

```python
print(response["messages"][-1].content)
```

- `response["messages"]` contains the full conversation history
- `response["messages"][-1]` is the agent's final message
- `.content` extracts the natural language response

---

<details>
<summary><strong>Final Code (Sending Tool Output and Getting the Final Response)</strong></summary>

```python
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langchain.tools import tool
import requests
from google.colab import userdata

# Initialize Google API key and model
google_api_key = userdata.get('GOOGLE_API_KEY')
model = init_chat_model("google_genai:gemini-2.5-flash", api_key=google_api_key)

# Initialize Tavily search tool
tavily_api_key = userdata.get('TAVILY_API_KEY')
skill_demand_tool = TavilySearch(
    max_results=5,
    search_depth="advanced",
    tavily_api_key=tavily_api_key,
)

# Invoke Tavily search tool
result = skill_demand_tool.invoke({"query": "generative ai skills demand 2025"})
print(result)

# Set up RapidAPI key and search jobs function
rapidapi_key = userdata.get('RAPIDAPI_KEY')

def search_jobs(skill: str, location: str) -> list:
    ""Search for jobs requiring a specific skill using JSearch API from RapidAPI.""
    print(f"\nCalling search_jobs tool")
    print(f"Searching jobs for: {skill} in {location}")

    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-key": rapidapi_key,
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }
    querystring = {
        "query": f"{skill} in {location}",
        "page": "1",
        "country": "in",
        "employment_types": "INTERN,FULLTIME",
        "job_requirements": "no_experience,under_3_years_experience"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    jobs = data.get("data", [])
    print(f"Found {len(jobs)} jobs\n")

    # Format and return job results
    result = []
    for job in jobs:
        result.append({
            "title": job.get("job_title"),
            "company": job.get("employer_name"),
            "location": job.get("job_city"),
            "apply_link": job.get("job_apply_link")
        })
    return result

# Define system prompt for the agent
system_prompt = ""You are a Skill-to-Career Mapping assistant that helps students understand skill demand and find matching job opportunities.

You have access to these tools:
- skill_demand_tool: Search for industry demand, salary insights, and career trends
- search_jobs: Find actual job listings requiring specific skills

Help the student by researching the skill they ask about and finding relevant opportunities.

Present results in a clean, readable format with clear sections and proper spacing. Include all job details with apply links. Don't use markdown format.""

# Create and invoke LangChain agent
from langchain.agents import create_agent

agent = create_agent(
    model=model,
    tools=[skill_demand_tool, search_jobs],
    system_prompt=system_prompt,
    debug=True
)

user_query = "What's the demand for generative ai in the industry and show me related job openings in India"

response = agent.invoke({
    "messages": [{"role": "user", "content": user_query}]
})
print(response["messages"][-1].content)

```

</details>

---

## How the Agent Loop Works

1. **Start**: Agent node calls the model with current messages
2. **Decision**: The model checks whether tool calls are required
3. **If Yes**:
   - Execute the required tools
   - Add the tool results as a ToolMessage
   - Loop back and call the model again with updated messages
4. **If No**:
   - Return the final answer (without tool calls)
5. **End**

The process repeats until no more tool calls are needed. The agent returns the final answer with skill insights and job listings.

![Project Screenshot](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat-course-projects/Pasted%20image.png)

---

## Try It Yourself

Challenge yourself by building similar agents:

| Agent Type | Input | What It Does |
|------------|-------|--------------|
| Interview Prep Agent | Role Name (e.g., "Data Analyst") | Find common interview questions + preparation tips |
| Salary Insights Agent | Job Title (e.g., "Full Stack Developer") | Fetch salary trends + top paying companies |
| Course Finder Agent | Skill name (e.g., "Gen AI") | Find free courses + certification options |
| Startup Jobs Agent | Domain (e.g., "Fin Tech") | Find startup job openings + company details |
| Skill Comparison Agent | Two skills (e.g., "React vs Angular") | Compare demand + job count + future scope |
| Location-Job Agent | City + Skill (e.g., "Bangalore, Python") | Find local jobs + remote options + avg salary |

You can also try replacing Tavily with other available search tools in LangChain like Brave Search, SearxNG Search, or Google Serper.

---

Here is the <a href="https://colab.research.google.com/drive/1ZISgZ-DnOgzPHTjjSXBAjoLV_kaypWEO#scrollTo=NV7NBkLzROXQ" target="_blank">
Building AI Agents with LangChain – Final Code
</a>