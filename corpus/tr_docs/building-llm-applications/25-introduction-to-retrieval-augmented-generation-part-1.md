# Introduction to Retrieval-Augmented Generation | Part 1

**Course:** Building LLM Applications  
**Topic:** Introduction to LangChain and Retrieval-Augmented Generation (RAG)  
**Unit ID:** `a44ec6b0cf9849a29a52abbe615ba215` | **Unit Number:** 25

---

# Introduction to Retrieval-Augmented Generation | Part 1

## Introduction

Imagine asking a Large Language Model (LLM) questions about your private documents:

-   What topics are in my university's Gen AI syllabus?
-   Summarize Attention Is All You Need research paper (without uploading the actual paper)
-   What's my college's leave policy?
-   Explain Chapter 5 in Gen AI (Without sharing the textbook)

LLMs are trained on massive amounts of public data, but they can't answer these questions because they don't have access to your personal or confidential documents.

### The Problem: Generic vs. Specific Information

If you ask an LLM a question that requires specific knowledge, you get a generic explanation from multiple sources across the internet. What you actually need are answers from **your** documents, not from generic internet data. The AI might give a confident answer, but it may not match what your specific document contains.

This is because of the following limitations of LLM's:

1.  **Knowledge Cutoff**: LLMs are trained on data available up to a certain point in time and do not have awareness of information created or updated after that training period.
2.  **Hallucinations**: When reliable information is missing, LLMs may generate responses that sound confident but are factually incorrect or not grounded in real data.
3.  **No Access to Private Data**: They cannot access your local files, internal wikis, or databases.

---

## Solutions to Overcome LLM Limitations

### 1. Give Context in Your Prompt

Manually add important information related to your question before asking the LLM.

```
"You are a helpful assistant. Answer the question ONLY from the provided context. If the context is insufficient, just say you don’t know.

{context}

Question: {question}"
```

**Advantages of giving context in the Prompt:**

-   No setup needed, works immediately.
-   Free to use.
-   Easy to implement.

**Disadvantages of giving context in the Prompt:**

-   Documents can be very long, you cannot paste everything.
-   LLMs have a limited context size.
-   Not practical when you have multiple documents.


### 2. Fine-Tune the LLM

Fine-tune the LLM using your specific documents so the knowledge becomes part of the model.


**Advantages of Fine Tuning the LLM:**

-   Model becomes an expert on your documents.
-   Fast responses because the knowledge is already built-in.
-   No need to include context in the prompt.

**Disadvantages of Fine Tuning the LLM:**

-   Expensive and computationally intensive.
-   Takes significant time to fine-tune.
-   If data changes, the model needs to be fine-tuned again.
</details>

---

## Retrieval-Augmented Generation (RAG)

**Retrieval-Augmented Generation (RAG)** is the process of optimizing the output of an LLM so it references an authoritative knowledge base outside of its training data sources before generating a response.

The process is broken down into three steps:

-   **(R)ETRIEVE**: Retrieve the most relevant information from your documents.
-   **(A)UGMENT**: Augment (add) that information to the user's question.
-   **(G)ENERATE**: Generate a better answer using both the retrieved information and the LLM's knowledge.

### How RAG Works

![DocuChat flow](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat-course-projects/Introduction%20to%20RAG%20_%20Part%201.png)

### Benefits of RAG
-   **Current Information**: Answers are based on up to date data.
-   **Decreased Hallucinations**: Responses are grounded in provided facts.
-   **Enhanced Accuracy**: Delivers more precise and relevant answers.
-   **Increased User Trust**: Users can see the source of the information.
-   **Domain-Specific**: Becomes an expert on a specific subject matter.

### Applications of RAG
-   Customer Support Chatbots
-   Financial Report Analysis
-   Medical Diagnosis Support
-   Legal Research Assistant
-   Enterprise Knowledge Search
-   Banking Policy Assistant
-   Employee Onboarding Assistant
-   Educational Tutoring
-   Video Content Chat

---

## Building DocuChat Application

**Scenario**: You have a 40-page research paper to read before tomorrow's seminar, but you need quick answers to questions like:

-   What are the key findings?
-   What are the limitations and future scope?
-   What is the main contribution of this paper?

For this, we will use the famous paper that introduced Transformers: <a href="https://arxiv.org/pdf/1706.03762.pdf" target="_blank">Attention Is All You Need</a>.

### Why Not Just Copy-Paste into an LLM?

LLMs have limited **context windows**, they cannot process entire documents at once. Even if they could, finding specific information buried in pages of text is inefficient. This is where RAG helps.

**DocuChat** will be a RAG-powered Q&A assistant that:
1.  **Retrieves** only the relevant paragraphs for your question.
2.  **Augments** your question with the actual paper content.
3.  **Generates** accurate answers grounded in the document.

### Frameworks for Building RAG Applications

Many frameworks simplify building RAG applications, including:

-   LangChain
-   LlamaIndex
-   Haystack
-   EmbedChain

We will use **LangChain**, as it simplifies the development process by providing a modular, standardized way to connect LLMs with external data sources.

### Building a RAG chatbot involves two main steps:
1.  **Indexing**: Preparing the documents for searching.
2.  **Retrieval and Generation**: Finding relevant data and generating an answer.

![DocuChat flow](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat-course-projects/Introduction%20to%20RAG%20_%20Part%201%20%282%29.png)

## 1. RAG Indexing

Indexing ensures that your external documents are organized into a multiple smaller parts, such that it can be quickly searched

Think of it like a librarian organizing a library:

- **Load :** Ingest documents from various sources so they are available for processing.

- **Split :** Break documents into smaller, structured sections to make them easier to search.

- **Embed :** Convert document sections into embeddings.

- **Store :** Store them in a searchable index for efficient retrieval.

Think of indexing like how a librarian organizes a library so books can be found quickly.

### RAG Indexing: Library Example

**Without Indexing**
Imagine walking into a library where books are not organized at all. When you ask,

*“Do you have a book on Generative AI?”*

the librarian has no catalog to refer to and must search through every shelf manually. Finding the book can take **hours**, even if it exists.

**With Indexing**
Now imagine a well-organized library:

* **Load** – The librarian first **collects all the books** available in the library.
* **Split** – The books are then **organized by subject and placed onto appropriate shelves**, making them easier to locate.
* **Embed** – A **searchable catalog** is created that records where each book or topic is located.
* **Store** – This catalog is **stored in the system** so it can be queried instantly.

When you ask again,

*“Do you have a book on Generative AI?”*

the librarian simply checks the catalog, walks directly to the correct shelf, and hands you the book **within seconds**.

This is exactly how **RAG indexing** works—by organizing documents in advance so relevant information can be retrieved quickly and efficiently when a question is asked.

### Step 1: Load the Document

LangChain provides over 100 **Document Loaders** for various file formats (`.pdf`, `.docx`, `.csv`) and sources (Google Drive, Webpages, Databases).

| Category  | Loaders                                      | Use Cases            |
|----------|-----------------------------------------------|----------------------|
| Files    | TextLoader, PDFLoader, DocxLoader, CSVLoader  | Local documents      |
| Webpages | WebBaseLoader, PlaywrightURLLoader             | Scraping websites    |
| Cloud    | GoogleDriveLoader, OneDriveLoader, S3Loader    | Cloud storage        |
| Databases| SQLDatabaseLoader, MongoDBLoader               | Querying databases   |

#### Setting Up the Environment

1.  Go to <a href="https://colab.research.google.com/" target="_blank" rel="noopener noreferrer">Google Colab</a>
2.  Create a new notebook.
<MultiLineNote>
Ensure you have a Google account created.
</MultiLineNote>

#### Install Dependencies
Our research paper is in PDF format, so we'll use `PyPDFLoader`.

- `langchain-community` is needed because it contains the tools (like PyPDFLoader) that help LangChain read documents such as PDFs.
- `pypdf` is needed because it actually opens the PDF file and extracts the text from it.

```bash
!pip install -qU langchain-community pypdf
```

#### Loading the PDF

The `PyPDFLoader` reads a PDF file and extracts the text content page by page.

- Specifying the PDF file path, creating a loader for the file, and loading the PDF by converting each page into a separate Document object.

```python
from langchain_community.document_loaders import PyPDFLoader

# Make sure you have uploaded the PDF to your Colab environment
file_path = "./attention_all_you_need.pdf"
loader = PyPDFLoader(file_path)
doc = loader.load()
```

- Printing the full list of documents created from the PDF, showing that the file has been successfully loaded.

```python
print(doc)
```

- Displaying metadata for the first page, such as:

    - Source file name
    - Page number
    - Total number of pages

```python
print(doc[0].metadata)
```

- Printing the actual text content extracted from the first page of the PDF.

```python
print(doc[0].page_content)
```

### Step 2: Split the Document

The loaded document pages are still too long for an LLM to process efficiently. We need to split them into smaller, meaningful chunks.

**Splitting** is the process of breaking large documents into smaller pieces so the retriever can effectively find relevant information. This respects LLM context window limits and improves retrieval accuracy.

**Advantages of Splitting: **

- Efficient Retrieval
- LLM Context Window Limits
- Improved Accuracy & Relevance
- Cost & Latency
- Semantic Coherence

#### **Different Ways of Splitting Documents**

1. **Length-Based Splitting**

    - This approach splits documents purely based on length, resulting in consistent chunk sizes.While simple and predictable, it may cut text in the middle of sentences or ideas.

2. **Text Structure-Based Splitting**

    - This strategy uses a hierarchy of natural text boundaries, trying each level in order:

        - Paragraphs (\n\n) — tried first
        - Sentences (., !, ?)
        - Words (spaces)
        - Characters

By respecting natural language structure whenever possible, this method helps preserve semantic coherence.

3. **Document Structure-Based Splitting**

    - For structured documents such as HTML, Markdown, or JSON, splitting is done based on their inherent structure. This keeps related content together and maintains logical grouping.

LangChain offers several **Text Splitters**,

| Text Splitter | How It Works |
|--------------|--------------|
| RecursiveCharacterTextSplitter | Splits on paragraphs, sentences, and words |
| CharacterTextSplitter | Splits on fixed character count |
| TokenTextSplitter | Splits based on token count |
| MarkdownTextSplitter | Respects markdown structure |
| PythonCodeTextSplitter | Respects code syntax |
| HTMLTextSplitter | Respects HTML tags |


We will use the `RecursiveCharacterTextSplitter`, which is great for generic text as it tries to split based on natural boundaries (paragraphs, sentences, words).

#### Install Dependencies
```bash
!pip install -qU langchain-text-splitters
```

#### Configure and Split
We'll split the document into chunks of 1000 characters with a 200-character overlap to maintain context between chunks.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
  chunk_size=1000,      
  chunk_overlap=200,    
)
all_splits = text_splitter.split_documents(doc)
print(all_splits)
print(f"Paper split into {len(all_splits)} sub-documents.")
print(f"Metadata: {all_splits[0].metadata}")
```

- <a href="https://colab.research.google.com/drive/1z7udEz5xr_HQswcGvB7bsdIt0556a69P#scrollTo=2q0NhFa7Hsf-" target="_blank">Final Code</a>