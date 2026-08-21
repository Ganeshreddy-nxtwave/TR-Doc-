# Introduction to Langchain

**Course:** Building LLM Applications  
**Topic:** Introduction to LangChain and Retrieval-Augmented Generation (RAG)  
**Unit ID:** `f7dd4c87bb15482b8268095d81d5775e` | **Unit Number:** 23

---

# Introduction to LangChain

## Introduction

In this unit, we will understand the challenges involved in building LLM applications and why a framework like LangChain is needed. We’ll explore how LangChain simplifies working with different LLM providers and learn about its core components. We will then focus on key components such as Models and Messages, and see how they help structure interactions with LLMs in a clean and consistent way.

### Manual and Repetitive Tasks in LLM Development
When working directly with LLM providers, developers are required to perform several repetitive tasks manually:

*   Rewrite tool schemas for different providers
*   Manage entire conversation flow manually
*   Handle tool execution logic ourselves
*   Format and structure model response

### The Provider Problem

Consider an application built using an LLM from Groq, such as the Weather Application. While the application works well with Groq, challenges arise when there is a need to, Switch to Claude (Anthropic), Gemini (Google), GPT-5 (OpenAI).

### Challenges in Switching Between Models
Switching from one LLM provider to another introduces multiple technical differences:

*   Different API structures
*   Different response formats
*   Different ways to handle tool calling
*   Different message formatting requirements

As a result, significant portions of the application code must be rewritten for each provider change.

### Growing Complexity in LLM Applications
As LLM applications evolve, additional requirements increases overall complexity.

Common challenges include:

*   Adding conversation memory
*   Integrating multiple tools
*   Handling errors

### Limitations of Implementing from Scratch
Building and maintaining LLM applications without a framework is:

*   Time-consuming
*   Error-prone
*   Difficult to maintain
*   Hard to scale

## Solution: We Need a Framework

A framework should:

*   Standardize working with different LLM providers
*   Provide pre-built components for common tasks
*   Enable easy switching between models and tools
*   Handle repetitive code automatically
*   Be well-tested and community-maintained

### Popular Frameworks available for building LLM Applications

*   LangChain
*   LlamaIndex
*   Haystack
*   Semantic Kernel
*   CrewAI

## What is LangChain?

LangChain is the easiest way to start building agents and applications powered by LLMs. It provides pre-built, modular components and standardized interfaces to build LLM applications quickly and efficiently.

### Why LangChain?
*   Most Widely Adopted: Over 1,20,000+ GitHub stars, used by thousands of companies.
*   Integrations for 100+ LLM Providers.

### LangChain Features
*   Comprehensive Documentation: LangChain has extensive tutorials, <a href="https://docs.langchain.com/oss/python/langchain/overview" target="_blank">documentation</a> and active community support.
*   Modular and Flexible: Use what you need, extend when necessary.

### Advantages of LangChain
*   Standardized Interfaces and Modularity
*   External Data Integration (RAG)
*   Agentic Capabilities and Automation
*   Active Community and Resources

### LangChain Core Components
*   Models
*   Messages
*   Tools
*   Agents

There are many more components present in LangChain.

## Models
LangChain’s standard model interfaces give us access to 100+ provider integrations, making it easy to experiment with and switch between models.

### Gemini model integration using LangChain

#### 1. Setting Up Environment
1.  Open <a href="https://colab.research.google.com/" target="_blank">Google Colab</a>
2.  Create a new notebook

<MultiLineNote>
Ensure you have a Google account created
</MultiLineNote>
#### 2.Installing the required pacakges
General Syntax(To install any LLM provider pacakge):

```bash
!pip install -U langchain-[provider-name]
```
Installing the `langchain-google-genai` package:

```bash
!pip install -U langchain-google-genai
```

#### 3. Securing the Gemini API Key
We will use Colab Secrets to hide our Gemini API Key from our code to use it securely.

#### 4. Configure the Gemini Model

```python
from google.colab import userdata
api_key=userdata.get('GEMINI_API_KEY')
```

#### 5. Importing Chat Model
LangChain provides `init_chat_model` to initialize chat from a chat model provider of our choice (e.g., Gemini).

```python
from langchain.chat_models import init_chat_model
```

#### Syntax:
```python
model = init_chat_model(
  <llm_provider_name>:<model-name>,  
  api_key=api_key,
)
```

#### Parameters
A chat model takes parameters that can be used to configure its behavior:


*   `llm_provider_name`: The name or identifier of the specific llm provider.
*   `model`: The name or identifier of the specific model you want to use with a provider.
*   `api_key`: The key required for authenticating with the model’s provider.


#### Initializing the Chat Model (Gemini Example)

```python
model = init_chat_model(
  "google_genai:gemini-2.5-flash",
  api_key=api_key,
)
```

#### 6. Making Request to the Model
LangChain provides `invoke()` method to make a request to the model with a single message or a list of messages.

```python
response = model.invoke("What are AI Agents?")
print(response)
```

#### Code to make a request to gemini-2.5-flash (gemini models) using LangChain

```python
from google.colab import userdata
api_key=userdata.get('GEMINI_API_KEY')

from langchain.chat_models import init_chat_model
model = init_chat_model(
    "google_genai:gemini-2.5-flash",
    api_key=api_key,

)
response = model.invoke("What are AI Agents?")
print(response)
```

## Messages

Messages are the fundamental unit of context for models in LangChain. They represent the input and output of models.

Messages are Objects that contains:

*   **Role**: Identifies the message type.
*   **Content**: Represents the actual content of the message.
*   **Metadata**: Optional fields such as response information, message IDs, and token usage.

#### Message Types
1.  System Message
2.  Human Message
3.  AI Message
4.  Tool Message

#### 1. Importing the HumanMessage and SystemMessage 

This step imports the message classes used by LangChain to represent different roles in a conversation. These message objects help structure the input sent to the chat model.

```python
from langchain.messages import HumanMessage, SystemMessage
```

#### 2. Creating a SystemMessage(System Prompt) 

The `SystemMessage` is used to define the behavior or role of the model. 

```python
system_msg = SystemMessage("You are a helpful assistant.")
```

#### 3. Creating a HumanMessage(User Query) 
The `HumanMessage` represents the user’s input or question that will be processed by the chat model.

```python
human_msg = HumanMessage("What are AI Agents?")
```

#### 4. Storing SystemMessage and HumanMessage in a list

```python
system_msg = SystemMessage("You are a helpful assistant.")
human_msg = HumanMessage("What are AI Agents?")
messages = [system_msg, human_msg]
```

### Final Code to make a request to gemini-2.5-flash (gemini models) using LangChain
The following code shows how to combine system and human messages, initialize the Gemini chat model using LangChain, and invoke the model with structured message input.

```python
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage

from google.colab import userdata
api_key=userdata.get('GEMINI_API_KEY')

system_msg = SystemMessage("You are a helpful assistant.")
human_msg = HumanMessage("What are Ai Agents?")
messages = [system_msg, human_msg]

model = init_chat_model(
  "google_genai:gemini-2.5-flash",
  api_key=api_key,
)

response = model.invoke(messages)
print(response.content)
```

### Final Code to make a request to llama-3.3-70b-versatile (LLM hosted in groq) using LangChain

The `langchain-groq` package is required to enable LangChain to communicate with LLMs present in Groq. It provides the necessary functionality to call models present in Groq using langchain.

1. Installing the `langchain-groq` package:

```bash
!pip install -U langchain-groq
```

<MultiLineNote>
Ensure you have a <a href="https://console.groq.com/keys" target="_blank">Groq API key</a> and place it in your Colab Secrets.</MultiLineNote>
This code initializes a llama-3.3-70b-versatile present in Groq using LangChain, securely loads the Groq API key from Colab Secrets, and sends structured system and user messages to the model.

```python
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage

from google.colab import userdata
api_key=userdata.get('GROQ_API_KEY')

system_msg = SystemMessage("You are a helpful assistant.")
human_msg = HumanMessage("What are Ai Agents?")
messages = [system_msg, human_msg]

model = init_chat_model(
  "groq:llama-3.3-70b-versatile",
  api_key=api_key,
)

response = model.invoke(messages)
print(response.content)
```

### Final Code to make a request to gpt-4.1 (openai models) using LangChain

The `langchain-openai` package is required to enable LangChain to communicate with OpenAI models. It provides the necessary functionality to initialize and invoke OpenAI models using LangChain.

1.Installing the `langchain-openai` package:

```bash
!pip install -U langchain-openai
```
<MultiLineNote> 
OpenAI APIs are not free to use. You need a paid OpenAI account to generate an <a href="https://platform.openai.com/settings/organization/api-keys" target="_blank">OpenAI API key</a> and place it in your Colab Secrets.</MultiLineNote>
This code initializes the gpt-4.1 model available from OpenAI using LangChain, securely loads the OpenAI API key from Colab Secrets, and sends structured system and user messages to the model.

```python
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage

from google.colab import userdata
api_key=userdata.get('OPENAI_API_KEY')

system_msg = SystemMessage("You are a helpful assistant.")
human_msg = HumanMessage("What are Ai Agents?")
messages = [system_msg, human_msg]

model = init_chat_model(
  "openai:gpt-4.1",
  api_key=api_key,
)

response = model.invoke(messages)
print(response.content)
```

As we build more advanced applications, we will be working with new components like Tools,Agents and other components in the LangChain ecosystem.