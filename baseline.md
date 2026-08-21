---
name: gen-ai-tr-doc-creator
description: Creates TR (Training Resource) reading materials for Generative AI, LLM, and AI courses. Triggers when the user asks to create, write, draft, or update a TR doc, reading material, or teaching resource for Sem or any Gen AI topic. Provides the complete student knowledge baseline from Sem1 and Sem2 so new content aligns naturally in depth, vocabulary, and progression.
---

# Gen AI TR Doc Creator

The reference files alongside this skill contain the complete Sem1 & Sem2 courseware — every reading material students have already completed. New Sem content is a natural continuation of this body of work.

> **New content is the next chapter, not a new book.** Students have built real AI applications, automated workflows, and deployed LLM-powered tools across 53 units. They think in terms of practical building, not theoretical learning.

## Student Knowledge Baseline

Students have completed three courses across Sem1 and Sem2. Everything below is assumed baseline.

### Generative AI (Sem1 — 21 units)

Students can use Gen AI tools practically in their daily life and have built real automated workflows.

| Domain | What Students Know | Reference |
|--------|-------------------|-----------|
| AI Fundamentals | Web search, deep research, voice I/O, screen sharing across ChatGPT, Claude, Gemini, Llama; choosing the right model for different tasks | [exploring-gen-ai-capabilities](generative-ai--06-exploring-gen-ai-capabilities.md) |
| Productivity Tools | Gamma AI (presentations), Code2Tutorial (repo understanding), ChatGPT Custom GPTs and Agent Mode | [productivity-power-up](generative-ai--12-productivity-power-up-with-ai-tools.md) |
| Prompt Engineering | RCATF framework (Role, Context, Action/Task, Format, Tone); zero-shot, one-shot, few-shot, chain-of-thought; LLM limitations and anti-hallucination techniques | [prompt-engineering-fundamentals](generative-ai--15-prompt-engineering-fundamentals.md), [advanced-prompt-engineering](generative-ai--19-advanced-prompt-engineering.md) |
| No-Code Automation | n8n platform (triggers, nodes, credentials), Google Sheets as data source, OAuth2 with Google APIs, social media automation (LinkedIn, Twitter) | [social-media-automation](generative-ai--17-building-social-media-content-automation-workflow.md) |
| AI Workflows | RSS feeds, HTTP Request nodes, SerpAPI integration, AI News Summarizer with Gmail delivery, schedule triggers | [news-summarizer-pt1](generative-ai--21-build-your-own-ai-news-summarizer-part-1.md), [news-summarizer-pt2](generative-ai--23-build-your-own-ai-news-summarizer-part-2.md) |
| Image Generation | Text-to-image, image-to-image, image-to-text using DALL-E 3, Gemini, Stable Diffusion; Kaggle environment setup | [image-generation](generative-ai--27-mastering-image-generation.md), [stable-diffusion](generative-ai--31-mastering-image-generation-with-stable-diffusion.md) |
| Audio Generation | AI audio tools, F5-TTS for voice cloning/synthesis | [audio-generation](generative-ai--33-mastering-ai-audio-generation.md), [f5-tts](generative-ai--38-mastering-ai-audio-generation-using-f5-tts.md) |
| AI Agents | Agent concepts, Learning Path Generator, agents with memory, MCP introduction, no-code app building | [intro-to-agents](generative-ai--33-introduction-to-ai-agents.md), [agent-with-memory](generative-ai--44-building-an-agent-with-memory.md), [mcp-intro](generative-ai--46-introduction-to-model-context-protocol.md) |
| Projects Built | Multi-part AI Shopping Assistant, AI News Summarizer, social media automation workflow | [shopping-assistant-pt1](generative-ai--40-build-your-own-ai-shopping-assistant-part-1.md), [shopping-assistant-pt2](generative-ai--42-build-your-own-ai-shopping-assistant-part-2.md) |

### Building REST APIs with Flask (Sem2 — 5 units)

Students can build and consume REST APIs in Python.

| Domain | What Students Know | Reference |
|--------|-------------------|-----------|
| Python Environment | Google Colab as dev environment, third-party packages, pip, API calls with `requests` | [intro-to-colab](building-rest-apis-with-flask--02-introduction-to-google-colab.md), [third-party-packages](building-rest-apis-with-flask--04-introduction-to-third-party-packages.md) |
| Flask | Routing, decorators, GET/POST endpoints, building product management REST APIs | [intro-to-flask](building-rest-apis-with-flask--06-introduction-to-flask.md), [building-rest-apis](building-rest-apis-with-flask--08-building-rest-apis-using-flask.md) |
| Frontend Integration | Fetch API consumption, CORS handling | [flask-frontend-integration](building-rest-apis-with-flask--10-integrating-flask-apis-in-frontend.md) |

### Building LLM Applications (Sem2 — 27 units)

Students can build, deploy, and evaluate full LLM-powered applications in Python.

| Domain | What Students Know | Reference |
|--------|-------------------|-----------|
| LLM Fundamentals | `google-genai` SDK for Gemini, Groq SDK for Llama; system prompts, generation settings (temperature, top_p, max_tokens); multi-turn conversations, streaming | [llm-python-pt1](building-llm-applications--05-building-llm-applications-using-python-part-1.md), [llm-python-pt2](building-llm-applications--07-building-llm-applications-using-python-part-2.md) |
| UI & Deployment | Gradio for interactive LLM interfaces; deploying to Hugging Face Spaces | [building-ui](building-llm-applications--09-building-ui-for-llm-applications.md), [deploying](building-llm-applications--11-deploying-llm-applications.md) |
| How LLMs Work | Transformer architecture, attention mechanism, tokenization, next-word prediction, training pipeline (pre-training, fine-tuning, RLHF) | [how-llms-work-pt1](building-llm-applications--13-understanding-how-llms-work-part-1.md), [how-llms-work-pt2](building-llm-applications--15-understanding-how-llms-work-part-2.md) |
| Tool Use & Function Calling | Function calling with Groq/Llama (tool schemas, JSON arguments); real-time Weather Application with OpenWeatherMap API; multi-tool orchestration | [function-calling](building-llm-applications--19-tool-use-function-calling-in-llms.md) |
| Advanced Prompting | Effective prompting in code: system prompts, structured outputs, prompt templates, dynamic construction | [prompting-techniques](building-llm-applications--21-effective-prompting-techniques.md) |
| LangChain | Why frameworks exist (provider switching, modularity); Models, Messages, Tools, Agents; `init_chat_model`, `ChatPromptTemplate`, `StrOutputParser`; tool decorators, `create_react_agent` | [intro-to-langchain](building-llm-applications--23-introduction-to-langchain.md) |
| RAG | Document loaders, text splitters, chunk strategies; embeddings (Google Generative AI); vector stores (FAISS), similarity search; RAG chain: retrieve → augment → generate | [rag-pt1](building-llm-applications--25-introduction-to-retrieval-augmented-generation-part-1.md), [rag-pt2](building-llm-applications--27-introduction-to-retrieval-augmented-generation-part-2.md) |
| AI Agents | ReAct pattern, LangChain agents with tool binding, memory agents (conversation buffer, summary memory), multi-step workflows | [langchain-agents](building-llm-applications--29-building-ai-agents-using-langchain.md), [memory-agents](building-llm-applications--31-building-memory-agents.md) |
| Context Engineering & MCP | Context engineering principles; MCP integration in LLM applications | [context-engineering](building-llm-applications--41-introduction-to-context-engineering.md), [integrating-mcp](building-llm-applications--43-integrating-mcp.md) |
| Multi-Agent Systems | CrewAI framework (agent roles, tasks, crews, delegation); Game Development Crew project | [crewai](building-llm-applications--45-building-multi-agent-systems-using-crew-ai.md), [game-dev-crew](building-llm-applications--47-building-a-game-development-crew.md) |
| LLM Evaluation | Evaluation metrics and methodologies; automated evaluation pipelines | [eval-pt1](building-llm-applications--49-introduction-to-llm-application-evaluation-part-1.md), [eval-pt2](building-llm-applications--51-introduction-to-llm-application-evaluation-part-2.md) |
| Local Models & Fine-Tuning | Running models locally (Ollama, llama.cpp); fine-tuning with LoRA, QLoRA | [running-locally](building-llm-applications--53-running-models-locally.md), [fine-tuning](building-llm-applications--55-fine-tuning-llms.md) |
| Projects Built | AI-Powered Conversational Interview Assistant (2 parts), RAG Agent, Study Assistant with personalities, Weather App with function calling | [interview-assistant-pt1](building-llm-applications--35-building-an-ai-powered-conversational-interview-assistant-part-1.md), [rag-agent](building-llm-applications--39-building-rag-agent-using-langchain.md) |

### Tools & Platforms in Student Repertoire

ChatGPT, Claude, Gemini, Llama (via Groq) | Google Colab, Kaggle | n8n, Gamma AI, Code2Tutorial | Flask, Gradio, Hugging Face Spaces | LangChain, CrewAI, FAISS | SerpAPI, OpenWeatherMap API, Google APIs (OAuth2) | F5-TTS, Stable Diffusion | Ollama

