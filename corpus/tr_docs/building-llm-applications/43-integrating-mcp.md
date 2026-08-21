# Integrating MCP

**Course:** Building LLM Applications  
**Topic:** Introduction to Context Engineering and MCP  
**Unit ID:** `e90b718f07ce41fbae4275c0c96230a1` | **Unit Number:** 43

---

# Introduction

In our previous sessions, we learned about Context Engineering, Context Engineering vs Prompt Engineering, four core techniques of Context Engineering, and common failures and fixes.

We built the SkillMap Agent using LangChain with Google Gemini, Tavily, and JSearch to deliver market insights and live job links, and also developed the DocuChat RAG application with a complete document-to-vector pipeline along with an AI-Powered Conversational Interview Assistant.

Now in this unit, we will learn how to integrate external tools using MCP in LangChain agents, configure MCP clients, and retrieve tools from MCP servers.

# Integrate external tools using MCP
## Model Context Protocol

MCP is a protocol for providing the context to the models.

*   **Model** — LLMs / AI Agents
*   **Context** — Information on how and when to use the tools
*   **Protocol** — Set of rules to follow for communication

MCP standardizes how AI applications interact with external systems:

*   Prompts
*   Tools
*   Resources

### Core Components

*   **MCP Host** — The application that contains the LLM
*   **MCP Client** — Maintains a dedicated connection to one MCP server to access the tools, resources or prompts
*   **MCP Server** — External systems that provide tools/capabilities that our agent can use (like Google Drive, Slack, LinkedIn)

###How to Integrate External Tools Using MCP in SkillMap Agent

**Initial Code**
<a href="https://colab.research.google.com/drive/1YscNUyhOFvp7MVuExmZ5I8aqv_8BwKMO#scrollTo=FjVX3AO0Tqdi" target="_blank">SkillMap Agent Colab</a>

## Integrating MCP in SkillMap Agent

### LangChain MCP Adapters

LangChain provides a package called `langchain-mcp-adapters` which allows agents to use tools defined on MCP servers.

```bash
!pip install langchain-mcp-adapters
```

### Configuring the MCP Client

`langchain-mcp-adapters` provides `MultiServerMCPClient` to manage connections to MCP servers simultaneously.

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
```

We need to initialize the `MultiServerMCPClient` with a dictionary defining the connection details for our MCP servers.

#### MultiServerMCPClient - Syntax

```python
client = MultiServerMCPClient(
    {
        "weather": {
            "transport": "How to communicate with the server",
            "url": "Where the MCP server is running",
            "headers": {
                "HTTP headers sent with each request",
            },
        }
    }
)
```

*  `client = MultiServerMCPClient` Creates a client object that can connect to multiple MCP servers
*   `"weather"` — A custom name you choose to identify this server

### Ways to Integrate MCP Servers

MCP supports two primary ways to communicate with an MCP server:

1.  **Streamable HTTP** — Uses HTTP POST requests for client-to-server communication
2.  **STDIO** — Uses standard input/output streams and recommended for local deployments

### Integrating MCP in SkillMap Agent

Let's start by setting up our MCP client for the SkillMap Agent:

```python
from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient(
    {
        "mcp_tavily": {
            "transport": "http",
            "url": "????",
        }
    }
)
```

## MCP Servers List

MCP servers are available from multiple sources:

* <a href="https://platform.composio.dev/" target="_blank">Composio</a>
* <a href="https://smithery.ai" target="_blank">Smithery</a>
* <a href="https://pipedream.com/" target="_blank">Pipedream</a>
* <a href="https://github.com/modelcontextprotocol/servers" target="_blank">MCP (Model Context Protocol Servers)</a>
* <a href="https://mcp.so/" target="_blank">MCP.so</a>

### Using Composio for MCP Servers

- **Composio** is a platform that provides MCP servers to connect tools to our agent.

## Configuring MCP Server

### Steps

1.  Get Composio MCP server URL for Tavily Search
2.  Configure and connect to the MCP server using the MCP Client

### Creating MCP Servers

- Go to MCP <a href="https://platform.composio.dev/" target="_blank">Composio</a> dashboard and login
2.  Go to MCP Configs and Create Config
- Select Dedicated Server and Create Server for Tavily with All Tools 
- Connect account with Tavily API key
- Copy the HTTP endpoint 


### Integrating MCP in SkillMap Agent with Composio URL

```python
from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient(
    {
        "mcp_tavily": {
            "transport": "http",
            "url": "https://backend.composio.dev/v3/mcp/a339a263-23f2-470b-9bea-e5ce36dc9531/mcp?user_id=pg-test-763f4e60-308c-417a-821c-c66b46b29d7e",
        }
    }
)
```

## Retrieving Tools from MCP

`MultiServerMCPClient` class provides methods that allows us to access:

*   Tools
*   Prompts
*   Other resources

Now that we have configured our MCP client, let's retrieve the tools available from the server.

`client.get_tools()` is an async method used to retrieve tools from MCP servers:

```python
tools = await client.get_tools()
```

### Why get_tools() is Async

The `client.get_tools()` method is asynchronous because:

*   **Network Communication** — Makes HTTP requests to fetch tools from the MCP server
*   **Non-blocking** — `await` lets other tasks run while waiting for the response

### Retrieving Tools

```python
async def skill_map_agent():
    mcp_tools = await client.get_tools()

  
```

### Combining MCP and LangChain Custom Tools

```python
async def skill_map_agent():
    mcp_tools = await client.get_tools()

    # Combine MCP tools with our custom tools
    all_tools = mcp_tools + [search_jobs]
```

### Providing Tools to Agent

```python
async def skill_map_agent():
    mcp_tools = await client.get_tools()

    # Combine MCP tools with our custom tools
    all_tools = mcp_tools + [search_jobs]

    agent = create_agent(
        model=model,
        tools=all_tools,
        system_prompt=system_prompt,
        debug=True
    )
```

### Updating System Prompt

```python
system_prompt = ""You are a Skill-to-Career Mapping assistant that helps students understand skill demand and find matching job opportunities.

You have access to these tools:
- search tool: Search for industry demand, salary insights, and career trends
- search_jobs: Find actual job listings requiring specific skills

Help the student by researching the skill they ask about and finding relevant opportunities.

Present results in a clean, readable format with clear sections and proper spacing. Include all job details with apply links. Don't use markdown format.""
""
```

### MCP Tools → LangChain Tools

LangChain converts MCP tools into LangChain tools, making them directly usable in any LangChain agent.

### Executing the Agent

- When using MCP tools, the agent may need to make network calls to the MCP server during execution.

- `ainvoke()` is the asynchronous version of `invoke()` that properly handles these network operations.

### Executing the Agent using ainvoke()

```python
from langchain.agents import create_agent

async def skill_map_agent():

  mcp_tools = await client.get_tools()

  # Combine MCP tools with our custom tools
  all_tools = mcp_tools+ [search_jobs]

  agent = create_agent(
    model=model,
  tools=all_tools,
  system_prompt=system_prompt,
  debug=True

  )
  user_query = "What's the demand for generative ai in the industry "

  response = await agent.ainvoke({
    "messages": [{"role": "user", "content": user_query}]
  })
  print(response["messages"][-1].content[0]["text"])

```

### Running the Async Function

```python
from langchain.agents import create_agent

async def skill_map_agent():

  mcp_tools = await client.get_tools()

  # Combine MCP tools with our custom tools
  all_tools = mcp_tools+ [search_jobs]

  agent = create_agent(
    model=model,
  tools=all_tools,
  system_prompt=system_prompt,
  debug=True

  )
  user_query = "What's the demand for generative ai in the industry "

  response = await agent.ainvoke({
    "messages": [{"role": "user", "content": user_query}]
  })
  print(response["messages"][-1].content[0]["text"])


await skill_map_agent()
```
`await skill_map_agent()`
*   This executes our async function and waits for it to complete
*   Google Colab supports top-level `await` (you can use `await` directly in notebook cells)
*   The agent will process the query, use the appropriate tools, and return the answer

## Using MCP Server Provided by Tavily Directly

- <a href="https://app.tavily.com/home" target="_blank">Tavily</a> is also providing a remote MCP server we can use directly in our application.



### Integrating Tavily MCP Server

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

client = MultiServerMCPClient(
    {
        "mcp_tavily": {
            "transport": "http",
            "url": "https://backend.composio.dev/v3/mcp/a339a263-23f2-470b-9bea-e5ce36dc9531/mcp?user_id=pg-test-763f4e60-308c-417a-821c-c66b46b29d7e",
        }
    }
)

```

## MCP: Advantages

*   **Plug & Play** — As the MCP ecosystem is rapidly growing, we can now directly integrate any MCP server without any additional work
*   **Flexibility and Scalability** — Can easily switch between different tools without rewriting integrations
*   **Context Rich** — Provides correct usage of tools with the clear context of the tools

Once we understand how to work with MCP, we can connect to any MCP-compatible resource using the same patterns and techniques.

### Final Code

```python
!pip install -U langchain-google-genai
!pip install langchain langchain-tavily
!pip install langchain-mcp-adapters

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.chat_models import init_chat_model
from google.colab import userdata

google_api_key = userdata.get('GEMINI_API_KEY')
model = init_chat_model("google_genai:gemini-2.5-flash", api_key=google_api_key)

from langchain_tavily import TavilySearch
from google.colab import userdata


tavily_api_key = userdata.get('TAVILY_API_KEY')
skill_demand_tool = TavilySearch(
    max_results=5,
    search_depth="advanced",
    tavily_api_key=tavily_api_key,
)

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

system_prompt = ""You are a Skill-to-Career Mapping assistant that helps students understand skill demand and find matching job opportunities.

You have access to these tools:
- search tool: Search for industry demand, salary insights, and career trends
- search_jobs: Find actual job listings requiring specific skills

Help the student by researching the skill they ask about and finding relevant opportunities.

Present results in a clean, readable format with clear sections and proper spacing. Include all job details with apply links. Don't use markdown format.""



client = MultiServerMCPClient(
    {
        "mcp_tavily": {
            "transport": "http",
            "url": "https://backend.composio.dev/v3/mcp/a339a263-23f2-470b-9bea-e5ce36dc9531/mcp?user_id=pg-test-763f4e60-308c-417a-821c-c66b46b29d7e",
        }
    }
)

from langchain.agents import create_agent

async def skill_map_agent():

  mcp_tools = await client.get_tools()

  # Combine MCP tools with our custom tools
  all_tools = mcp_tools+ [search_jobs]

  agent = create_agent(
    model=model,
  tools=all_tools,
  system_prompt=system_prompt,
  debug=True

  )
  user_query = "What's the demand for generative ai in the industry "

  response = await agent.ainvoke({
    "messages": [{"role": "user", "content": user_query}]
  })
  print(response["messages"][-1].content[0]["text"])


await skill_map_agent()
```