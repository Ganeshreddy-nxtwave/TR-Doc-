# Tool Use & Function Calling in LLMs

**Course:** Building LLM Applications  
**Topic:** Tools Use & Function Calling in LLMs  
**Unit ID:** `90a7b2db297e4a1c9dfb0edec279fe6f` | **Unit Number:** 19

---

# Tool Use & Function Calling in LLMs

## Introduction

So far, we have explored how to build applications that provide answers based on a Large Language Model's existing knowledge. But what happens when we need our application to access real-time data or interact with external systems? This session introduces **Tool Use**, also known as **Function Calling**, a powerful feature that allows LLMs to connect with external resources to perform tasks and retrieve dynamic information.

---

## The Problem: LLM Knowledge Limitations

LLMs are trained on vast datasets, but this knowledge is static and has a "knowledge cutoff" date. They do not have access to any information or events that occurred after their training was completed.

If you ask an LLM for current, real-time information without access to external tools, it cannot provide an accurate answer.

<details>
<summary><strong>Example: Asking for Current Information</strong></summary>

Let's ask a model for the latest iPhone, instructing it not to use a web search.

```
"Can you recommend the latest iPhone model (do not use web search)?"
```

Models like GPT, Gemini, and Claude will likely provide information about models that were the latest at the time their training data was collected, not the actual latest model available today.

</details>

This limitation prevents us from building applications that require real-time data, such as:

-   Current weather conditions
-   Live stock prices
-   Latest news headlines
-   Real-time sports scores
-   Today's calendar events

The solution to this is **Tool Calling**.

---

## What is Tool/Function Calling?
**Tool calling** (function calling) is a  powerful feature that allows LLMs to interact with external resources

This is different from how we used tools in a no-code platform like n8n. In n8n, the platform itself

- Manages tool connections. 
- Formats tool inputs / outputs
- Coordinates between LLM and tools

Now let us understand how we can integrate tools to LLMs in Python

---

## Let's Build: A Real-Time Weather Application

To understand how function calling works in practice, we will build a Python application that can provide the current weather for any city.

### Initial Code

we will be using the the following code to make calls to LLMs.



```bash
!pip install groq
```

```python
from google.colab import userdata
from groq import Groq

client = Groq(
  api_key=userdata.get('GROQ_API_KEY')
)

response = client.chat.completions.create(
  messages=[ {
    "role": "user",
    "content": "What is the current weather in hyderabad",
  }], model="llama-3.3-70b-versatile",
)
print(response.choices[0].message.content)
```



### Prerequisites

-   A **<a href="https://console.groq.com/keys" target="_blank">Groq API Key</a>** to access LLMs.
-   An **<a href="https://home.openweathermap.org/api_keys" target="_blank">OpenWeatherMap API Key</a>** to get real-time weather data.
- The URL Endpoint:

    ```
    http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={api_key}
    ```

<MultiLineNote>
Your OpenWeather API key will be activated automatically within 2 hours upon successful registration
</MultiLineNote>
-   Python environment with the `groq` and `requests` packages installed.

### Platform Support for Function Calling


Many LLM platforms now provide support for function calling, allowing their models to interact with external tools:

-   **OpenAI**: GPT models (e.g., `gpt-5`)
-   **Claude**: Anthropic's models (e.g., `claude-opus-4.5`)
-   **Gemini**: Google's models (e.g., `gemini-3-pro-preview`)
-   **Cohere**: Cohere's models (e.g., `command-a-03-2025`)
-   **Groq**: Supports various models, including Llama (e.g., `llama-3.3-70b-versatile`)
-   **Mistral AI**: Mistral's models (e.g., `mistral-large-latest`)

Let us use **Groq** for our weather application:

-   Groq is a platform that provides multiple AI models, including llama models.
-  Groq enables function calling by accepting a list of functions(tools) and returning structured JSON arguments from supported models

## Step 1: Create the Weather Function

First, we need a Python function that can fetch weather data from the OpenWeatherMap API. We'll use the `requests` library to make the API call.

<details>
<summary><strong>Code to Get Weather Information</strong></summary>

This function takes a `location`, calls the weather API, and returns a simplified dictionary with the key weather details.

```python
import json
import requests
from google.colab import userdata

def get_weather(location):
  api_key = userdata.get('WEATHER_API_KEY')
  url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={api_key}"

  response = requests.get(url)
  data = response.json()
  if data.get("cod") == 200:
    return json.dumps({
      "location": location,
      "temperature": data["main"]["temp"],
      "description": data["weather"][0]["description"]
    })
  else:
    return json.dumps({"Oops! Something went wrong."})

# Example usage:
# print(get_weather("Hyderabad"))
```

</details>

<MultiLineNote>
This `get_weather` function is just one example. You can replace it with any functionality you need - sending emails, calculations, or calling any other external API.
</MultiLineNote>

## Step 2: Define the Tool for the LLM

### What is a Tool?

A tool is a piece of functionality that we explicitly tell the model it has access to.When generating a response, the model decides whether it needs information from a tool to complete the task.

### Understanding Tools: Functionality We Give the Model

<img src="https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat-course-projects/Copy%20of%20Tool%20Use%20%26%20Function%20Calling%20in%20LLMs%20%281%29.png" alt=">


This flow ensures that tools are used only when required, and simple questions are answered directly without unnecessary external calls.

<MultiLineNote>
**Important:** The LLM does not execute the tool — it only decides which tool to use and with what inputs.
</MultiLineNote>

### Examples of Tools

Tools can represent many kinds of real-world functionality:

-   Get current weather for a location
-   Send emails
-   Update spreadsheets
-   Schedule calendar events
-   Search the web

Each of these tools gives the LLM capabilities beyond its training data.

### Defining a Tool for an LLM

To describe a function in a format that an LLM understands, we use a JSON schema structure.

This schema contains:

-   Function metadata
-   Parameter specifications

### Tool Definition Structure

A tool definition consists of the following key fields:

| Field       | Purpose                               |
| :---------- | :------------------------------------ |
| `name`        | Function name the LLM will call       |
| `description` | What the function does                |
| `parameters`  | What inputs the function needs        |
| `properties`  | Details about each parameter          |
| `required`    | Which parameters are mandatory        |

### Tool Definition for get_weather function
<details>
<summary><strong>Code</strong></summary>

```python
tools = [
  {
    "type": "function",
    "function": {
      "name": "get_weather",
      "description": "Get current weather for a city",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "City name like Mumbai, London"
          }},
        "required": ["location"]
      }}}
]
```
</details>

### Sending the Tool Definition to the Model

Once you have defined your tool(s), you provide them to the LLM (Large Language Model) when making a Chat Completion request. Let’s break down the main parameters involved in this API call:

- **model**: Specifies which language model version to use (e.g., `"llama-3.3-70b-versatile"`). Different models may have different capabilities and costs.
- **messages**: A list of messages representing the conversation history. Each message is a dictionary with fields like "role" (either "user", "assistant", "system", or "tool") and "content" (the message text). Keeping the full chat history enables the LLM to generate coherent and contextually relevant responses.
- **tools**: The list of tool definitions provided to the LLM—these specify how to call function to get weather details.
- **tool_choice**: Determines whether the model decides automatically ("auto") when to call a tool, or if you want to force a specific tool call.

Here’s how a complete request using these parameters might look:

<details>
<summary><strong>Code</strong></summary>

```python
from google.colab import userdata
from groq import Groq
import json
import requests

client = Groq(
    api_key = userdata.get('GROQ_API_KEY')
)

def get_weather(location):
 api_key = userdata.get('WEATHER_API_KEY')
 url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={api_key}"
 response = requests.get(url)
 data = response.json()

 if data["cod"] == 200:
   return {
     "location": location,
     "temperature": data["main"]["temp"],
     "description": data["weather"][0]["description"]
   }
 else:
   return {"Oops! Something went wrong."}

tools = [
  {
    "type": "function",
    "function": {
      "name": "get_weather",
      "description": "Get current weather for a city",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "City name like Mumbai, London"
            }
            },
      "required": ["location"]
           }
       }
   }
]

llm_messages = [
  {
    "role": "system",
    "content": "You are a weather assistant. Use get_weather function when asked about weather."
  },
  {
    "role": "user",
    "content": "What's the weather in Mumbai?"
  }
]

response = client.chat.completions.create(
  model="llama-3.3-70b-versatile",
  messages=llm_messages,
  tools=tools,
  tool_choice="auto"
)

print(response.choices[0].message)

```
- The model evaluates the user message. If it determines a tool call is needed, it includes the tool call in the response rather than a plain text answer.
- Otherwise, `.message.content` contains a direct natural language response from the LLM.
- Examining the full `response` lets you inspect tool call details or troubleshoot unexpected behavior.

</details>

### Understanding the LLM Response

<details>
<summary><strong>Tool Call(Response from LLM)</strong></summary>

```python
{
  "id": "chatcmpl-8275582c-f79c-4af1-8f69-8bb8cfc5ba90",
  "choices": [
    {
      "finish_reason": "tool_calls",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": null,
        "role": "assistant",
        "annotations": null,
        "executed_tools": null,
        "function_call": null,
        "reasoning": null,
        "tool_calls": [
          {
            "id": "y5nmt906p",
            "function": {
              "arguments": "{\"location\":\"Hyderabad\"}",
              "name": "get_weather"
            },
            "type": "function"
          }
        ]
      }
    }
  ],
  "created": 1766490111,
  "model": "llama-3.3-70b-versatile",
  "object": "chat.completion",
  "mcp_list_tools": null,
  "service_tier": "on_demand",
  "system_fingerprint": "fp_93b5f9e564",
  "usage": {
    "completion_tokens": 15,
    "prompt_tokens": 229,
    "total_tokens": 244,
    "completion_time": 0.045290652,
    "completion_tokens_details": null,
    "prompt_time": 0.011681956,
    "prompt_tokens_details": null,
    "queue_time": 0.008271432,
    "total_time": 0.056972608
  },
  "usage_breakdown": null,
  "x_groq": {
    "id": "req_01kd5g7z11efkvagwg4xz2fy9c",
    "debug": null,
    "seed": 1715653078,
    "usage": null
  }
}


```

</details>

Instead of directly returning weather information, the LLM may return a structured response requesting a tool.This response is called a **Tool Call**.


When the LLM decides to use a tool, it always returns structured information, including:

-   Function name to call
-   Parameters to use



### Step 3: Handle the LLM's Tool Call

When using tool/function calling, the LLM (Language Model) does **not** execute functions or access tools by itself. Instead, if it determines that an external tool (in this case, a function like `get_weather`) is needed to answer a user's question, it returns a special structured response called a **tool call**. This tool call specifies which function to run and with which parameters.

<details>
<summary><strong>First API Call and Handling the Response</strong></summary>

```python
from google.colab import userdata
from groq import Groq
import json
import requests

client = Groq(
    api_key = userdata.get('GROQ_API_KEY')
)

def get_weather(location):
 api_key = userdata.get('WEATHER_API_KEY')
 url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={api_key}"
 response = requests.get(url)
 data = response.json()

 if data["cod"] == 200:
   return {
     "location": location,
     "temperature": data["main"]["temp"],
     "description": data["weather"][0]["description"]
   }
 else:
   return {"Oops! Something went wrong."}

tools = [
  {
    "type": "function",
    "function": {
      "name": "get_weather",
      "description": "Get current weather for a city",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "City name like Mumbai, London"
            }
            },
      "required": ["location"]
           }
       }
   }
]

llm_messages = [
  {
    "role": "system",
    "content": "You are a weather assistant. Use get_weather function when asked about weather."
  },
  {
    "role": "user",
    "content": "What's the weather in Mumbai?"
  }
]

response = client.chat.completions.create(
  model="llama-3.3-70b-versatile",
  messages=llm_messages,
  tools=tools,
  tool_choice="auto"
)

response_message = response.choices[0].message

if response_message.tool_calls:
  tool_call = response_message.tool_calls[0]
  arguments = json.loads(tool_call.function.arguments)
  location = arguments['location']
  weather_data = get_weather(location)

  final_response = client.chat.completions.create(
      messages = llm_messages,
      model = "llama-3.3-70b-versatile",
      tools = tools,
      tool_choice = "auto"
  )
```

- When the user asks for the weather, the LLM receives the message along with the tool definition (the schema of what can be called).
- Rather than trying to answer directly, the LLM may respond with a **tool call** indicating "I want you to call `get_weather` with `{"location": "Mumbai"}`".
- The code checks for this tool call, extracts the requested parameters from the tool call's arguments, and then executes the actual Python function (`get_weather`) outside of the LLM.
- This is necessary because LLMs can't access the internet, APIs, or your environment; you must run the code they suggest and then supply the result back to them.

</details>

### Step 4: Send the Results Back to the LLM

Once we've received the actual weather information from our `get_weather` function (stored in `weather_data`), we need to provide this result back to the LLM. The LLM can then use the returned data to generate a natural language response for the user.

We append the LLM's tool call request and our function's result to the message history, then make a final API call.

```python
llm_messages.append(response_message)

  llm_messages.append({
      "role": "tool",
      "tool_call_id": tool_call.id,
      "content": json.dumps(weather_data)
  })
 ```
<details>

<summary><strong>Final Code (Sending Tool Output and Getting the Final Response)</strong></summary>
 
```python
from google.colab import userdata
from groq import Groq
import json
import requests

client = Groq(
    api_key = userdata.get('GROQ_API_KEY')
)

def get_weather(location):
 api_key = userdata.get('WEATHER_API_KEY')
 url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={api_key}"
 response = requests.get(url)
 data = response.json()

 if data.get("cod") == 200:
    return json.dumps({
      "location": location,
      "temperature": data["main"]["temp"],
      "description": data["weather"][0]["description"]
    })
  else:
    return json.dumps({"Oops! Something went wrong."})

tools = [
  {
    "type": "function",
    "function": {
      "name": "get_weather",
      "description": "Get current weather for a city",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "City name like Mumbai, London"
            }
            },
      "required": ["location"]
           }
       }
   }
]

llm_messages = [
  {
    "role": "system",
    "content": "You are a weather assistant. Use get_weather function when asked about weather."
  },
  {
    "role": "user",
    "content": "What's the weather in Mumbai?"
  }
]

response = client.chat.completions.create(
  model="llama-3.3-70b-versatile",
  messages=llm_messages,
  tools=tools,
  tool_choice="auto"
)

response_message = response.choices[0].message

if response_message.tool_calls:
  tool_call = response_message.tool_calls[0]
  arguments = json.loads(tool_call.function.arguments)
  location = arguments['location']
  weather_data = get_weather(location)

  llm_messages.append(response_message)

  llm_messages.append({
      "role": "tool",
      "tool_call_id": tool_call.id,
      "content": json.dumps(weather_data)
  })

  final_response = client.chat.completions.create(
      messages = llm_messages,
      model = "llama-3.3-70b-versatile",
      tools = tools,
      tool_choice = "auto"
  )

  print(final_response.choices[0].message.content)
```
</details>
---

## Flow Summary

Here is a summary of the entire function calling flow:

1.  **Developer**: Defines a `get_weather` function in Python.
2.  **Developer**: Describes the function to the LLM using a JSON schema (the `tools` list).
3.  **User**: Asks, "What’s the weather in Hyderabad?".
4.  **LLM**: Receives the prompt and the tool definition. It decides the `get_weather` tool is needed and returns a tool call for `get_weather("Hyderabad")`.
5.  **Developer(get_weather Function code)**: Catches the tool call, executes the `get_weather("Hyderabad")` function, which calls the OpenWeatherMap API.
6.  **Developer(get_weather Function code)**: Sends this result back to the LLM in a new API call, including the full conversation history.
7.  **LLM**: Receives the temperature data and generates the final response: "It’s currently 26°C in Hyderabad."