# Building RAG Agent Using LangChain

**Course:** Building LLM Applications  
**Topic:** Building AI-Powered Conversational Interview Assistant and RAG Agent Using LangChain  
**Unit ID:** `8eb12476a433466cb7eda3e2b5f57936` | **Unit Number:** 39

---

# Introduction

In the previous unit, we built an AI Powered Conversational Interview Assistant. In this unit, we will understand RAG Agents and adding agent capabilities to our DocuChat application.

## DocuChat Application

<details>
<summary>RAG DocuChat Application Code</summary>


```python
! pip install -qU  langchain langchain-huggingface sentence_transformers

from langchain_huggingface import HuggingFaceEmbeddings

# Initialize free, local embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

```

```python
!pip install -qU langchain-chroma

from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)
document_ids = vector_store.add_documents(documents=all_splits)
sample = vector_store.get(limit=1, include=["embeddings", "documents"])
print(f"Embedding dimensions: {len(sample['embeddings'][0])}")
print(sample)
print(document_ids[:3])
```

```python
from langchain.chat_models import init_chat_model
from google.colab import userdata

api_key = userdata.get('GEMINI_API_KEY')
model = init_chat_model(
   "google_genai:gemini-2.5-flash",
   api_key=api_key,
)

def docu_chat(user_query):
  context, source_docs = retrieve_context(user_query, k=2)
  system_message = f""You are a helpful chatbot.
                     Use only the following pieces of context to answer the 
                     question. Don't makeup any new information: {context} ""

  messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_query}
  ]
  response = model.invoke(messages)
     return {
  "answer": response.content,
  "source_documents": source_docs,
  "context_used": context
}
result = docu_chat( "Explain what is the use of decoders in transformers?")
print(result)
print(result["answer"])
```

</details>

Have you ever asked our RAG DocuChat application a question like:

```
Compare the attention mechanism from the paper with recent improvements like Flash Attention, and tell me which approach would be better for my college project
```

Or imagine having two vector databases — one has syllabus (topics, units, learning goals) and another has old exam papers (questions, answers):

``` 
Which Unit 3 topics appear most frequently in exams?
```

### What Should the Application Do?

Should it:

*   Just search the document once and give an answer?
*   Think, plan, search multiple sources, and reason through the answer?

### Testing the DocuChat

When we test our DocuChat with the question:

```
Compare the attention mechanism from the paper with recent improvements like Flash Attention, and tell me which approach would be better for my college project
```
**RESULT!** 

```
{'answer': 'The provided context describes the attention mechanism introduced in the paper "Attention is All you Need," but it does not contain information about recent improvements like Flash Attention.\n\nBased on the provided text, the attention mechanism proposed in "Attention is All you Need" is:\n*   A novel, simple network architecture based solely on an attention mechanism, completely removing recurrence and convolutions.\n*   It includes scaled dot-product attention and multi-head attention.\n*   Experiments on machine translation tasks showed these models to be superior in quality, more parallelizable, and required significantly less time to train compared to dominant sequence transduction models based on recurrent or convolutional neural networks.\n*   For example, a single model with 165 million parameters achieved 27.5 BLEU on English-to-German translation and 41.1 BLEU on English-to-French translation, outperforming existing best ensemble and single state-of-the-art results, respectively.\n\nTherefore, based solely on the provided text, I cannot compare the attention mechanism from the paper with Flash Attention or recommend which approach would be better for your college project, as information on Flash Attention is not available in the given context.', 'source_documents': [Document(id='7bf8f651-b938-4953-b42e-f95bd5d706e7', metadata={'author': 'Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin', 'page': 0, 'editors': 'I. Guyon and U.V. Luxburg and S. Bengio and H. Wallach and R. Fergus and S. Vishwanathan and R. Garnett', 'firstpage': '5998', 'type': 'Conference Proceedings', 'subject': 'Neural Information Processing Systems http://nips.cc/', 'language': 'en-US', 'total_pages': 11, 'book': 'Advances in Neural Information Processing Systems 30', 'creator': 'PyPDF', 'description-abstract': 'The dominant sequence transduction models are based on complex recurrent orconvolutional neural networks in an encoder and decoder configuration. The best performing such models also connect the encoder and decoder through an attentionm echanisms.  We propose a novel, simple network architecture based solely onan attention mechanism, dispensing with recurrence and convolutions entirely.Experiments on two machine translation tasks show these models to be superiorin quality while being more parallelizable and requiring significantly less timeto train. Our single model with 165 million parameters, achieves 27.5 BLEU onEnglish-to-German translation, improving over the existing best ensemble result by over 1 BLEU. On English-to-French translation, we outperform the previoussingle state-of-the-art with model by 0.7 BLEU, achieving a BLEU score of 41.1.', 'description': 'Paper accepted and presented at the Neural Information Processing Systems Conference (http://nips.cc/)', 'published': '2017', 'moddate': '2018-02-12T21:22:10-08:00', 'date': '2017', 'title': 'Attention is All you Need', 'lastpage': '6008', 'start_index': 1610, 'created': '2017', 'publisher': 'Curran Associates, Inc.', 'source': '/content/attention_is_all_you_need.pdf', 'creationdate': '', 'eventtype': 'Poster', 'producer': 'PyPDF2', 'page_label': '1'}, page_content='transduction problems such as language modeling and machine translation [ 29, 2, 5]. Numerous\nefforts have since continued to push the boundaries of recurrent language models and encoder-decoder\narchitectures [31, 21, 13].\n∗Equal contribution. Listing order is random. Jakob proposed replacing RNNs with self-attention and started\nthe effort to evaluate this idea. Ashish, with Illia, designed and implemented the ﬁrst Transformer models and\nhas been crucially involved in every aspect of this work. Noam proposed scaled dot-product attention, multi-head\nattention and the parameter-free position representation and became the other person involved in nearly every\ndetail. Niki designed, implemented, tuned and evaluated countless model variants in our original codebase and\ntensor2tensor. Llion also experimented with novel model variants, was responsible for our initial codebase, and\nefﬁcient inference and visualizations. Lukasz and Aidan spent countless long days designing various parts of and'), Document(id='e833a9df-5536-4f7c-80a7-d328fdb621e2', metadata={'page': 8, 'lastpage': '6008', 'subject': 'Neural Information Processing Systems http://nips.cc/', 'moddate': '2018-02-12T21:22:10-08:00', 'page_label': '9', 'language': 'en-US', 'producer': 'PyPDF2', 'eventtype': 'Poster', 'date': '2017', 'description-abstract': 'The dominant sequence transduction models are based on complex recurrent orconvolutional neural networks in an encoder and decoder configuration. The best performing such models also connect the encoder and decoder through an attentionm echanisms.  We propose a novel, simple network architecture based solely onan attention mechanism, dispensing with recurrence and convolutions entirely.Experiments on two machine translation tasks show these models to be superiorin quality while being more parallelizable and requiring significantly less timeto train. Our single model with 165 million parameters, achieves 27.5 BLEU onEnglish-to-German translation, improving over the existing best ensemble result by over 1 BLEU. On English-to-French translation, we outperform the previoussingle state-of-the-art with model by 0.7 BLEU, achieving a BLEU score of 41.1.', 'author': 'Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin', 'start_index': 0, 'editors': 'I. Guyon and U.V. Luxburg and S. Bengio and H. Wallach and R. Fergus and S. Vishwanathan and R. Garnett', 'description': 'Paper accepted and presented at the Neural Information Processing Systems Conference (http://nips.cc/)', 'published': '2017', 'title': 'Attention is All you Need', 'total_pages': 11, 'firstpage': '5998', 'book': 'Advances in Neural Information Processing Systems 30', 'creationdate': '', 'type': 'Conference Proceedings', 'created': '2017', 'source': '/content/attention_is_all_you_need.pdf', 'creator': 'PyPDF', 'publisher': 'Curran Associates, Inc.'}, page_content='Table 3: Variations on the Transformer architecture. Unlisted values are identical to those of the base\nmodel. All metrics are on the English-to-German translation development set, newstest2013. Listed\nperplexities are per-wordpiece, according to our byte-pair encoding, and should not be compared to\nper-word perplexities.\nN d model dff h d k dv Pdrop ϵls\ntrain PPL BLEU params\nsteps (dev) (dev) ×106\nbase 6 512 2048 8 64 64 0.1 0.1 100K 4.92 25.8 65\n(A)\n1 512 512 5.29 24.9\n4 128 128 5.00 25.5\n16 32 32 4.91 25.8\n32 16 16 5.01 25.4\n(B) 16 5.16 25.1 58\n32 5.01 25.4 60\n(C)\n2 6.11 23.7 36\n4 5.19 25.3 50\n8 4.88 25.5 80\n256 32 32 5.75 24.5 28\n1024 128 128 4.66 26.0 168\n1024 5.12 25.4 53\n4096 4.75 26.2 90\n(D)\n0.0 5.77 24.6\n0.2 4.95 25.5\n0.0 4.67 25.3\n0.2 5.47 25.7\n(E) positional embedding instead of sinusoids 4.92 25.7\nbig 6 1024 4096 16 0.3 300K 4.33 26.4 213\nIn Table 3 rows (B), we observe that reducing the attention key size dk hurts model quality. This')], 'context_used': "Source: {'author': 'Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin', 'page': 0, 'editors': 'I. Guyon and U.V. Luxburg and S. Bengio and H. Wallach and R. Fergus and S. Vishwanathan and R. Garnett', 'firstpage': '5998', 'type': 'Conference Proceedings', 'subject': 'Neural Information Processing Systems http://nips.cc/', 'language': 'en-US', 'total_pages': 11, 'book': 'Advances in Neural Information Processing Systems 30', 'creator': 'PyPDF', 'description-abstract': 'The dominant sequence transduction models are based on complex recurrent orconvolutional neural networks in an encoder and decoder configuration. The best performing such models also connect the encoder and decoder through an attentionm echanisms.  We propose a novel, simple network architecture based solely onan attention mechanism, dispensing with recurrence and convolutions entirely.Experiments on two machine translation tasks show these models to be superiorin quality while being more parallelizable and requiring significantly less timeto train. Our single model with 165 million parameters, achieves 27.5 BLEU onEnglish-to-German translation, improving over the existing best ensemble result by over 1 BLEU. On English-to-French translation, we outperform the previoussingle state-of-the-art with model by 0.7 BLEU, achieving a BLEU score of 41.1.', 'description': 'Paper accepted and presented at the Neural Information Processing Systems Conference (http://nips.cc/)', 'published': '2017', 'moddate': '2018-02-12T21:22:10-08:00', 'date': '2017', 'title': 'Attention is All you Need', 'lastpage': '6008', 'start_index': 1610, 'created': '2017', 'publisher': 'Curran Associates, Inc.', 'source': '/content/attention_is_all_you_need.pdf', 'creationdate': '', 'eventtype': 'Poster', 'producer': 'PyPDF2', 'page_label': '1'}\nContent: transduction problems such as language modeling and machine translation [ 29, 2, 5]. Numerous\nefforts have since continued to push the boundaries of recurrent language models and encoder-decoder\narchitectures [31, 21, 13].\n∗Equal contribution. Listing order is random. Jakob proposed replacing RNNs with self-attention and started\nthe effort to evaluate this idea. Ashish, with Illia, designed and implemented the ﬁrst Transformer models and\nhas been crucially involved in every aspect of this work. Noam proposed scaled dot-product attention, multi-head\nattention and the parameter-free position representation and became the other person involved in nearly every\ndetail. Niki designed, implemented, tuned and evaluated countless model variants in our original codebase and\ntensor2tensor. Llion also experimented with novel model variants, was responsible for our initial codebase, and\nefﬁcient inference and visualizations. Lukasz and Aidan spent countless long days designing various parts of and\n\nSource: {'page': 8, 'lastpage': '6008', 'subject': 'Neural Information Processing Systems http://nips.cc/', 'moddate': '2018-02-12T21:22:10-08:00', 'page_label': '9', 'language': 'en-US', 'producer': 'PyPDF2', 'eventtype': 'Poster', 'date': '2017', 'description-abstract': 'The dominant sequence transduction models are based on complex recurrent orconvolutional neural networks in an encoder and decoder configuration. The best performing such models also connect the encoder and decoder through an attentionm echanisms.  We propose a novel, simple network architecture based solely onan attention mechanism, dispensing with recurrence and convolutions entirely.Experiments on two machine translation tasks show these models to be superiorin quality while being more parallelizable and requiring significantly less timeto train. Our single model with 165 million parameters, achieves 27.5 BLEU onEnglish-to-German translation, improving over the existing best ensemble result by over 1 BLEU. On English-to-French translation, we outperform the previoussingle state-of-the-art with model by 0.7 BLEU, achieving a BLEU score of 41.1.', 'author': 'Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin', 'start_index': 0, 'editors': 'I. Guyon and U.V. Luxburg and S. Bengio and H. Wallach and R. Fergus and S. Vishwanathan and R. Garnett', 'description': 'Paper accepted and presented at the Neural Information Processing Systems Conference (http://nips.cc/)', 'published': '2017', 'title': 'Attention is All you Need', 'total_pages': 11, 'firstpage': '5998', 'book': 'Advances in Neural Information Processing Systems 30', 'creationdate': '', 'type': 'Conference Proceedings', 'created': '2017', 'source': '/content/attention_is_all_you_need.pdf', 'creator': 'PyPDF', 'publisher': 'Curran Associates, Inc.'}\nContent: Table 3: Variations on the Transformer architecture. Unlisted values are identical to those of the base\nmodel. All metrics are on the English-to-German translation development set, newstest2013. Listed\nperplexities are per-wordpiece, according to our byte-pair encoding, and should not be compared to\nper-word perplexities.\nN d model dff h d k dv Pdrop ϵls\ntrain PPL BLEU params\nsteps (dev) (dev) ×106\nbase 6 512 2048 8 64 64 0.1 0.1 100K 4.92 25.8 65\n(A)\n1 512 512 5.29 24.9\n4 128 128 5.00 25.5\n16 32 32 4.91 25.8\n32 16 16 5.01 25.4\n(B) 16 5.16 25.1 58\n32 5.01 25.4 60\n(C)\n2 6.11 23.7 36\n4 5.19 25.3 50\n8 4.88 25.5 80\n256 32 32 5.75 24.5 28\n1024 128 128 4.66 26.0 168\n1024 5.12 25.4 53\n4096 4.75 26.2 90\n(D)\n0.0 5.77 24.6\n0.2 4.95 25.5\n0.0 4.67 25.3\n0.2 5.47 25.7\n(E) positional embedding instead of sinusoids 4.92 25.7\nbig 6 1024 4096 16 0.3 300K 4.33 26.4 213\nIn Table 3 rows (B), we observe that reducing the attention key size dk hurts model quality. This\n\n"}
The provided context describes the attention mechanism introduced in the paper "Attention is All you Need," but it does not contain information about recent improvements like Flash Attention.

Based on the provided text, the attention mechanism proposed in "Attention is All you Need" is:
*   A novel, simple network architecture based solely on an attention mechanism, completely removing recurrence and convolutions.
*   It includes scaled dot-product attention and multi-head attention.
*   Experiments on machine translation tasks showed these models to be superior in quality, more parallelizable, and required significantly less time to train compared to dominant sequence transduction models based on recurrent or convolutional neural networks.
*   For example, a single model with 165 million parameters achieved 27.5 BLEU on English-to-German translation and 41.1 BLEU on English-to-French translation, outperforming existing best ensemble and single state-of-the-art results, respectively.

Therefore, based solely on the provided text, I cannot compare the attention mechanism from the paper with Flash Attention or recommend which approach would be better for your college project, as information on Flash Attention is not available in the given context.

```
### Let's Break Down The Question

| Information Needed | Where to Find It? |
|---|---|
| Attention Mechanism Details | PDF (Vector Database) |
| Flash Attention (Different) | NOT in 2017 paper! |
| Recent Improvements | NOT in 2017 paper! |
| Project Recommendations | Needs reasoning from BOTH |

### What Our RAG DocuChat Actually Does

Question → Search Vector DB (ONE time) → Get top 2 chunks → Send to LLM → Answer 

**The Fixed Pipeline Problem:** No reasoning or external search

### What We Need

Our DocuChat is like a librarian who brings you the first book they find.

But what we need is a research assistant who:

*   Understands your question deeply
*   Plans how to find the best answer
*   Searches multiple times if needed
*   Puts everything together logically
*   Searches web if answer is not found

### The Solution: What If RAG Could Think?

This is where <b>RAG Agent</b> comes in!

*   **Analyze** the question and break it into sub-tasks
*   **Decide** which tool to use for each sub-task
*   **Execute** multiple searches across different sources
*   **Reason** through all the gathered information
*   **Synthesize** a comprehensive final answer

## What is RAG Agent?

**RAG Agent is a framework** that **enhances traditional RAG systems** by incorporating intelligent agents **to handle complex tasks** and make **decisions dynamically**.

## Traditional RAG VS Agentic RAG

**RAG (Fixed Pipeline):**

User Question → Retrieve (Always, ONE time) → Generate (Always) → Answer

**Agentic RAG (Intelligent Agent):**

User Question → Agent THINKS: "What do I need?" → Agent DECIDES: "Which tool to use?" → Agent ACTS: Executes tool(s) → Agent REASONS: Generates answer

### RAG vs Agentic RAG Comparison

| Feature | RAG | Agentic RAG |
|---|---|---|
| Retrieves context? | ✅ Yes | ✅ Yes |
| Plans next steps? | ❌ No | ✅ Yes |
| Multi-turn reasoning? | ❌ No | ✅ Yes |
| Uses tools/APIs? | ❌ No | ✅ Yes |
| Task autonomy | ❌ Only Q&A | ✅ Takes steps to complete a task |

## Let's Add Agent Capabilities to Our DocuChat RAG Application

### What We Already Have

Our existing DocuChat code has:

*   Document Loading (PyPDF Loader)
*   Text Splitting (Recursive Character-Text Splitter)
*   Vector Store (Chroma DB)
*   Embeddings (Hugging Face-Embeddings)
*   LLM (Gemini Model)

### What We Are Building

We will add the following to our existing DocuChat:

*   **Retrieval Tool** (Searches our PDF)
*   **Web Search Tool** (Searches the internet)
*   **Agent** (Decides which tool to use)

### Steps to be Followed

1.  Create RAG Agent
2.  Convert Retrieval Function to a Tool
3.  Add Web Search Tool
4.  Execute the Agent

## Step 1: Create RAG Agent

We now have two tools, but someone needs to decide which tool to use!

####The Agent can:

*   Analyze the user's question
*   Decide which tool(s) to call
*   Execute the tools
*   Generate the final answer

### Configure the Agent

```python
from langchain.agents import create_agent

agent = create_agent(
    model=model,
    tools=[retrieve_from_pdf, web_search_tool],
    system_prompt=system_prompt,
)
```

### Define System Prompt

```python
system_prompt = ""You are a helpful research assistant with access to two tools:

1. retrieve_from_pdf: Use this to find information from the
   "Attention Is All You Need" research paper

2. TavilySearch: Use this to find current information
   not in the paper (recent events, updates, etc.)

Strategy:
- For questions about the paper content → use retrieve_from_pdf
- For questions about recent events or topics not in the paper → use TavilySearch
- DON'T make up things 
""
```

## Step 2: Convert Retrieval Function to a Tool

### Why Do We Need This?

Currently, our retrieval function is just a Python function:

```python
def retrieve_context(query: str, k: int = 2):

    retrieved_docs = vector_store.similarity_search(query, k=k)

    # Build context string
    docs_content = "
    for doc in retrieved_docs:
        docs_content += f"Source: {doc.metadata}\n"
        docs_content += f"Content: {doc.page_content}\n\n"

    return docs_content, retrieved_docs
```

**Problem:** The agent cannot use this function directly.

**Solution:** Convert to Tool — the agent can understand and call it.

### Recap: Tool Syntax

```python
@tool
def function_name(parameter: str) -> str:
    ""
    Short description of what this tool does.
    ""
    return f"Processed: {parameter}"
```

*   `@tool`**Tool decorator** — Registers the function as a LangChain tool
*   `(parameter: str) -> str:`**Type annotations** — Define the input schema and expected output type for the LLM
*   `    ""
    Short description of what this tool does.
    ""` **Docstring** — Describes the tool's purpose to help the LLM decide when to use it

### Adding the Tool Decorator

```python
from langchain.tools import tool

@tool
def retrieve_from_pdf(query: str) -> str:
    ""Retrieve information from the Attention Is All You Need research paper.""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    docs_content = "
    for doc in retrieved_docs:
        docs_content += f"Source: {doc.metadata}\n"
        docs_content += f"Content: {doc.page_content}\n\n"
    return docs_content
```

We add the `@tool` decorator, return type `str`, and a descriptive docstring — together these help the agent understand what this tool does and when to use it.

## Step 3: Add Web Search Tool

### Why Do We Need Web Search?

Our retrieval tool can only search documents stored in the vector database. To answer questions about recent events not covered in our documents, we need a tool that can search the web.

### Solution: Tavily Search

To find info about latest research papers, we'll use **Tavily Search** — a search engine built specifically for AI agents (LLMs) delivering real-time, accurate, and factual results at speed.

### Install the Tavily Package

```bash
!pip install langchain-tavily
```

```python
from langchain_tavily import TavilySearch

tavily_api_key = userdata.get('TAVILY_API_KEY')

web_search_tool = TavilySearch(
    max_results=5,
    search_depth="advanced",
    tavily_api_key=tavily_api_key,
)
```

## Step 4: Execute the Agent

### Executing the Agent

To execute our agent, we use the invoke method which triggers the complete workflow.

All agents include a sequence of messages in their state. To invoke the agent, pass a new message with the user's query.

### Invoke the Agent

```python
user_query = ""Compare the attention mechanism from the paper with recent improvements like Flash Attention, and tell me which approach would be better for my college project.""

response = agent.invoke({
    "messages": [{"role": "user", "content": user_query}]
})

print(response["messages"][-1].content)
```


###Final Code

```python
! pip install -qU  langchain langchain-huggingface sentence_transformers

from langchain_huggingface import HuggingFaceEmbeddings

# Initialize free, local embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)
from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)
document_ids = vector_store.add_documents(documents=all_splits)
sample = vector_store.get(limit=1, include=["embeddings", "documents"])
print(f"Embedding dimensions: {len(sample['embeddings'][0])}")
print(sample)
print(document_ids[:3])

```
```python
!pip install -qU langchain-google-genai
!pip install langchain langchain-tavily

from langchain.chat_models import init_chat_model
from google.colab import userdata
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_tavily import TavilySearch


api_key=userdata.get('GEMINI_API_KEY')


model = init_chat_model(
    "google_genai:gemini-2.5-flash",
    api_key=api_key,

)


@tool
def retrieve_from_pdf(query: str) -> str:
    ""Retrieve information from the Attention Is All You Need research paper.""

    retrieved_docs = vector_store.similarity_search(query, k=2)

    docs_content = "
    for doc in retrieved_docs:
        docs_content += f"Source: {doc.metadata}\n"
        docs_content += f"Content: {doc.page_content}\n\n"

    return docs_content
    

tavily_api_key = userdata.get('TAVILY_API_KEY')
web_search_tool = TavilySearch(
    max_results=3,
    search_depth="advanced",
    tavily_api_key=tavily_api_key
)

system_prompt = ""You are a helpful research assistant with access to two tools:

1. retrieve_from_pdf: Use this to find information from the
   "Attention Is All You Need" research paper

2. TavilySearch: Use this to find current information
   not in the paper (recent events, updates, etc.)

Strategy:
- For questions about the paper content → use retrieve_from_pdf
- For questions about recent events or topics not in the paper → use TavilySearch
""


agent = create_agent(
    model=model,
    tools=[retrieve_from_pdf, web_search_tool],
    system_prompt=system_prompt
)

user_query = "Compare the attention mechanism from the paper with recent improvements like Flash Attention, and tell me which approach would be better for my college project"

response = agent.invoke({
    "messages": [{"role": "user", "content": user_query}]
})

print(response["messages"][-1].content)
```