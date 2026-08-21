# Running Models Locally

**Course:** Building LLM Applications  
**Topic:** Running Models locally and Fine-Tuning LLMs  
**Unit ID:** `5398860e63a94110bef30a4ca0a5f42c` | **Unit Number:** 53

---

# Introduction

In our previous session, we learned about Evaluating LLM Applications using LLM-as-a-Judge, Introduction to Evaluation Frameworks, DeepEval, and Evaluating Study Assistant using DeepEval.

In this unit, we will focus on running models locally, hardware requirements and popular models that can be run locally, tools like Ollama and LM Studio for this purpose, and provide a step-by-step guide on using Ollama.

---

## Running Models Locally

> How many of you have used ChatGPT or Google Gemini in the last week?

### Imagine

*   Every time you use ChatGPT, your data goes to someone else's computer (their servers)
*   What if you're in a place with no internet?
*   What if you don't want to pay monthly fees for AI tools?
*   What if you want complete privacy — no one sees your data?

### Running AI Without the Internet

> Have you ever felt running chatGPT on your own laptop, without internet?

You can download an AI model and run it on your own computer — no internet required, completely offline access.

### Key Benefits

*   **Privacy** — Your data never leaves your computer
*   **Speed** — No internet delays, responses are instant
*   **Offline Access** — Works even without internet
*   **Cost** — Free to use after initial setup (no subscription needed)
*   **Control** — You decide which open source model to use

### What Do You Need?

1.  A Powerful Computer
2.  An AI Model
3.  A Local Tool which runs AI model

---

## A Powerful Computer

### Requirements

| Component | Minimum Requirement | Recommended |
|---|---|---|
| RAM | 8 GB | 16 GB or more |
| Storage | 10 GB free space | 50 GB+ for multiple models |
| Processor | Modern CPU | CPU with GPU support |

### Understanding Model Sizes

AI models come in different sizes. Think of it like video quality:

*   **Small (480p)** — Works on any phone, but not very clear
*   **Medium (1080p)** — Looks good, needs decent phone
*   **Large (4K)** — Amazing quality, needs powerful device

###AI models work the same way:

| Model Size | RAM Needed | Quality | Best For |
|---|---|---|---|
| 3B (3 billion) | 4 GB | Good for simple tasks | Older laptops |
| 7B (7 billion) | 8 GB | Great for most tasks | Average laptops |
| 13B (13 billion) | 16 GB | Excellent quality | Good laptops |
| 70B (70 billion) | 64 GB+ | Near ChatGPT quality | Powerful desktops |



<div style="border: 1px solid #4CAF50; padding: 8px 12px; border-radius: 6px; background-color: #f6fff6; display: inline-block;">
"B" stands for Billion Parameters — it's like how many "brain cells" the AI has!
</div>

----

##An AI Model

### Popular Models You Can Run Locally

**LLaMA 3 (Made by: Facebook/Meta)**

*   Sizes: 8B, 70B
*   Good at: General conversations, Coding, Reasoning

**Mistral (Made by: Mistral AI — French company)**

*   Size: 7B
*   Good at: Fast responses, Efficient

**Phi-3 (Made by: Microsoft)**

*   Size: 3.8B
*   Good at: Smart for its small size

**CodeLlama (Made by: Meta)**

*   Size: 7B
*   Good at: Writing code, Explaining code

----

## Tools for Running Models Locally

These are free software that help us download and run AI models:

*   **Ollama**
*   **LM Studio**
*   **GPT4All**
*   …many more

## Ollama

### What is it?

Ollama is like an app store for AI models. It makes downloading and running AI as simple as installing an app.

### Why it's great?

*   One-line installation
*   Supports many popular models
*   Works on Windows, Mac, and Linux
*   Free and open-source

### Step-by-Step Guide Using Ollama

1.  Install Ollama
2.  Download/Pull a Model
3.  Run the Model

### Step 1: Install Ollama

1.  Visit: <a href="https://ollama.com" target="_blank">Ollama</a>
2.  Download for your operating system (Windows, macOS, or Linux)
3.  Install it like any other software

### Step 2: Download/Pull a Model

Open your terminal:

*   <b>Windows</b> — Search for "Command Prompt" or "PowerShell"
*   <b>Mac/Linux</b> — Search for "Terminal"

<MultiLineNote>
Before running Ollama, close memory-intensive applications.
</MultiLineNote>

**Check Memory Usage**

```bash
# On Linux, check memory usage
free -h

# On macOS
vm_stat

# On Windows
wmic OS get FreePhysicalMemory
```

**Download a Model**

Type this simple command:

```bash
ollama pull deepseek-r1:8b
```

This downloads the deepseek-r1:8b model to your computer. It may take a few minutes depending on your internet speed.

### Step 3: Run the Model

Type this simple command

```bash
ollama run deepseek-r1:8b
```

That's it! You now have an AI chatbot running entirely on your PC. Type your questions and get instant responses. No internet needed after download!

**Managing Models**

You can list all installed models:

```bash
ollama list
llama3
mistral
gemma
```

Removing a model:

```bash
ollama rm <model-name>
ollama rm llama3
```

Models stored locally after pulling can be reused across all apps.

** Integrate Local Models Using**

*   LangChain
*   Python Library
*   Local Server

----

## LM Studio

### What is it?

LM Studio is a desktop application with a nice visual interface. No typing commands needed!

### Why it's great

*   Beautiful, easy-to-use interface
*   Browse & download models with one click
*   Shows how much memory each model needs
*   Chat interface looks like ChatGPT

**Perfect for:**

*   Not interested in typing commands
*   Want to try many different models
*   Clicking over Coding

### Installing and Running Models with LM Studio

**Step 1:** Download LM Studio — Visit <a href="https://lmstudio.ai" target="_blank">LM Studio</a> and download for your operating system

**Step 2:** Install LM Studio — Install it like any other software

**Step 3:** Click on the "Search" or "Discover" icon and Download Model

**Step 4:** Go to the Chat interface and Load the Model

**Step 5:** Chat and Configure Settings

----

## Limitations to Know About

### Hardware Requirements

*   Better models need more powerful computers
*   Gaming laptops or desktops work best
*   Older computers can only run smaller models

### Initial Setup

*   First download can be large (2-40 GB per model)
*   Need to learn basic command line (for some tools)

### Quality Gap

*   Local models are good but not always as smart as GPT
*   The gap is closing fast though!

### No Real-Time Information

*   Local models only know what they were trained on
*   Can't search the internet for current news