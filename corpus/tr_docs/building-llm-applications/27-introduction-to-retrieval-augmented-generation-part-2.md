# Introduction to Retrieval-Augmented Generation | Part 2

**Course:** Building LLM Applications  
**Topic:** Introduction to LangChain and Retrieval-Augmented Generation (RAG)  
**Unit ID:** `2a378c0db84342fcbfbacd750467e370` | **Unit Number:** 27

---

#Introduction

In the previous unit, we covered LLM Limitations, Building a RAG Application, and RAG Indexing (loading and splitting documents). In this unit, we will focus on creating embeddings, storing them in a vector database, retrieving relevant chunks, and generating a final response using a Large Language Model (LLM).


## Introduction to RAG: Indexing

The first step is to **index** your documents for easy retrieval. This includes:

- **Loading the document**
- **Splitting** it into manageable chunks
- **Creating embeddings** that convert text into numerical representations
- **Storing** these embeddings in a vector store

##Create Embeddings
We have split our document into multiple chunks. Each split contains a portion of our document's information



**Challenge** -  How do we quickly find relevant chunks when a user asks a question?
**Solution** - We convert chunks into numbers (embeddings) that let us search by meaning instantly

### How it works

- Convert text into numbers (vectors)
- Compare vectors mathematically
- Vectors that are closer in value => Text that is closer in meaning

###What Are Embeddings
Embedding model converts text into numerical vectors (embeddings) that capture semantic meaning

**Similar meanings = Similar vectors**

###Embedding Models in LangChain

LangChain supports many embedding providers:

| Provider        | Model Examples           |
|-----------------|--------------------------|
| OpenAI          | text-embedding-3-small   |
| Cohere          | embed-english-v3.0       |
| HuggingFace     | all-mpnet-base-v2        |
| Google Vertex   | textembedding-gecko      |
| Ollama          | nomic-embed-text         |
| Voyage AI       | voyage-2                 |

###Why we Choose Hugging Face

- Completely free
- High quality
- Privacy

##Install Dependencies

```python
! pip install -qU langchain langchain-huggingface sentence_transformers

```
## Initialize Embeddings

```python
! pip install -qU  langchain langchain-huggingface sentence_transformers

from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
  model_name = "sentence-transformers/all-mpnet-base-v2"
)

```

##Why We Need a Vector Store

Now we need to create and store embeddings so that we can search later.

### Create Embeddings
- Convert each split into a vector.

For example, we split a document into smaller parts and create embeddings for each part. These embeddings are numerical vectors representing the semantic meaning of the content.

- Example vectors from splits:
  - `[0.3, 0.4, 0.1, 1.8, 1.1...]`
  - `[0.7, 1.4, 2.1, 4.8, 1.8...]`
  - `[1.2, 0.3, 1.2, 4.1, 1.8...]`

### Store Embeddings
- Save all vectors in a Vector Store (a database for embeddings).

Once the embeddings are created, they are stored in a vector database. The vectors can later be retrieved for similarity comparisons or answering queries.

- Example stored vectors:
  - `[0.3, 0.4, 0.1, 1.8, 1.1...]`
  - `[0.7, 1.4, 2.1, 4.8, 1.8...]`
  - `[1.2, 0.3, 1.2, 4.1, 1.8...]`

##What is Vector Store

A vector store is a specialized storage system

- Stores vectors along with their metadata
- Allows quick searching by similarity
- Returns results ranked by how similar they are

##Vector Store Providers

- ChromaDB
- FAISS
- Pinecone
- Weaviate
- Qdrant
- Milvus
- Astra DB

LangChain provides a unified interface for vector stores

- Add documents to the store
- Remove stored documents by ID
- Query for semantically similar documents

###Install Dependencies

```python
!pip install -qU langchain-chroma

```

###Initialize ChromaDB

```python
from langchain_chroma import Chroma

vector_store = Chroma(
  collection_name="research_collection",      
  embedding_function=embedding_model,            
  persist_directory="./chroma_langchain_db" 
)
document_ids = vector_store.add_documents(documents=all_splits)

sample = vector_store.get(limit=1, include=["embeddings", "documents"])
print(sample)
print(document_ids[:3])
```


### Save to Vector Store

#### What Gets Created

- **Your Project Folder/**
  - `chroma_langchain_db/`
    - chroma.sqlite3 – `Database file`
  - `attention_is_all_you_need.pdf` – `Collection data`

## RAG: Indexing

Now our document is indexed and stored !

- The actual RAG process, which takes the user query at run time and retrieves the relevant data from the index, then passes that to the model

Steps to be Followed

- Retrieve relevant Chunks
- Generate answers using LLM

## Retrieving Relevant Chunks

###The Goal

- Our vector store contains chunks from the research paper 

###The Challenge

- Which chunks contain the answer? We need to find the relevant chunks  to our question

###How Do We Find Relevant Chunk 

- User question converted to embedding
- Embedding compared with stored embeddings 
- Similar embeddings are identified
- Corresponding text chunks are returned

###What is Similarity Scoring

- The retriever uses cosine similarity a mathematical way to measure how close two vectors are in meaning-space

## Retrieve Relevant Chunks

### What is Similarity Scoring

**Imagine Two Arrows (Vectors):**

#### If they point the SAME direction  
Similarity = 1.0 (100% match)

#### If they point OPPOSITE directions  
Similarity = -1.0 (opposite meaning)

#### If they point somewhat the same way  
Similarity = 0.75 (75% match)

- The system now compares the question vector with all chunk vectors in the database

###Similarity Search Method

Similarity search method is a technique used to find and retrieve pieces of data that are semantically (by meaning) similar to a given query, rather than matching by exact keywords

<b> `vector_store.similarity_search(query, k=2) `</b>

k=2 Finds top 2 most similar chunks

####Building the Retrieval Function

```python
def retrieve_context(query: str, k: int = 2):
  retrieved_docs = vector_store.similarity_search(query, k=k)
```

####Extracting Document Content

```Python
def retrieve_context(query: str, k: int = 2):
  retrieved_docs = vector_store.similarity_search(query, k=k)

  docs_content = "
  for doc in retrieved_docs:
    docs_content += f"Source: {doc.metadata}\n"
    docs_content += f"Content: {doc.page_content}\n\n"

  return docs_content, retrieved_docs
```

###Retrieved Chunks Alone Aren't Enough

- Raw text needs to be synthesized
- Information needs to be explained clearly
- Answer should be natural and conversational

##Generate answers using LLM

####The LLM’s Role

- Read the retrieved context
- Understand the user's question
- Generate accurate answer

###Installing Dependencies

<b>syntax</b>

```syntax
!pip install -U langchain-[provider-name]
```

```Python
!pip install -U langchain-google-genai

```

###Initializing The Model

```python 
from langchain.chat_models import init_chat_model
from google.colab import userdata

api_key = userdata.get('GEMINI_API_KEY')
model = init_chat_model(
   "google_genai:gemini-2.5-flash",
   api_key=api_key,
)
```

###Defining the Query function

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
```

###Setting Up the LLM Instructions 

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
```

###Invoking LLM And Getting Results

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
result = docu_chat( "Explain what is the use of decoders 
in transformers?")
print(result)
print(result["answer"])
```

##Complete DocuChat Flow

![DocuChat Overview](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat-course-projects/docuchat.png)

## Try It Yourself

### Textbook Assistant
Any chapter from your textbook

- Explain binary search
- What are the types of joins in SQL?

### Notes Q&A Bot
Your own class notes

- What did we cover about arrays?
- Explain recursion from my notes

### Exam Question Bank Assistant
Previous year question papers

- What topics have most questions?
- Show questions on sorting algorithms

###Final code

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