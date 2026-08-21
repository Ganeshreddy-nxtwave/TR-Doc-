# AI in the Real World

**Course:** Building LLM Applications  
**Topic:** Building AI Agents Using LangChain and Memory Agents  
**Unit ID:** `14004159821b40d1af4a77d355cbbd89` | **Unit Number:** 33

---

# AI In The Real World

## Introduction

Till now, we've explored LLMs, RAG systems, Agents, and Memory. Now here's the exciting part: The concepts you just learned? They're already solving REAL problems for millions of people worldwide.

## What AI Can Do

### ChatGPT Identifies Rare Disease

A 4-year-old boy named Alex had chronic pain for 3 YEARS. 17 doctors couldn't figure it out. His mother copied symptoms and MRI results into ChatGPT which suggested "This could be tethered cord syndrome." A neurosurgeon confirmed it, surgery was performed, and the pain was gone.

<MultiLineQuickTip text={AI Concept}>

LLM pattern recognition from training data — same concept you learned!
</MultiLineQuickTip>

*   Full Story: <a href="https://www.today.com/health/mom-chatgpt-diagnosis-pain-rcna101843" target="_blank">TODAY.com</a>

### More Real-World Cases

*   **Saved a Man at 3 AM**: A Norwegian man sent home with “acid reflux.” Described symptoms to Grok, which flagged appendicitis.
    *   Source: <a href="https://www.teslarati.com/man-credits-grok-ai-with-saving-his-life-after-er-missed-near-ruptured-appendix/" target="_blank">Teslarati</a>
*   **Detected Blood Cancer**: 27-year-old (Marly) with night sweats. Tests normal. Chat GPT suggested cancer. A year later: Hodgkin lymphoma confirmed
    *   Source: <a href="https://www.newsbytesapp.com/news/science/chatgpt-diagnoses-woman-s-blood-cancer-before-doctors/story" target="_blank">NewsBytes</a>
*   **Found hidden Thyroid Cancer**: Doctors said acid reflux. ChatGPT suggested Hashimoto’s. Thyroid cancer was discovered.
    *   Source: <a href="https://www.foxnews.com/health/woman-says-chatgpt-saved-her-life-helping-detect-cancer-which-doctors-missed" target="_blank">Fox News</a>

### Amazon Q - Enterprise RAG at Scale

*   **Problem**: AWS has over 100,000 pages of documentation. Finding exact answers can take 30+ minutes.
*   **Solution**: Amazon Q gives complete answers with code examples, best practices, and source links.
<MultiLineQuickTip text={AI Concept}>
This is an enterprise-scale RAG system trained on 17 years of AWS content, exactly what your DocuChat does but at a larger scale.
LLM pattern recognition from training data — same concept you learned!
</MultiLineQuickTip>

*   **Technical Stack**:
    *   Built on Amazon Bedrock
    *   Uses multiple foundation models
    *   Retrieves from docs, blogs, and support articles
*   Official: <a href="https://aws.amazon.com/q/" target="_blank">AWS Amazon Q</a>
*   Technical Docs: <a href="https://aws.amazon.com/blogs/machine-learning/bringing-agentic-retrieval-augmented-generation-to-amazon-q-business/" target="_blank">RAG Reference</a>

### RAG - More Real-World Cases

*   **Amazon Rufus**: A shopping assistant trained on the product catalog and reviews. It uses over 80,000 Trainium/Inferentia chips.
    *   Source: <a href="https://aws.amazon.com/blogs/machine-learning/scaling-rufus-the-amazon-generative-ai-powered-conversational-shopping-assistant-with-over-80000-aws-inferentia-and-aws-trainium-chips-for-prime-day/" target="_blank">AWS Blog - Rufus Architecture</a>
*   **Perplexity**: An answer engine using Vespa.ai for its vector store. It serves 22 million users and handles 780 million monthly queries using hybrid retrieval and semantic search.
    *   Source: <a href="https://vespa.ai/perplexity/" target="_blank">Vespa.ai - How Perplexity Works</a>

### Tool Calling in Action

*   **Claude Web Search**: Ask "What's the weather today?" and Claude calls `web_search()` to return results with citations.
    *   Source: <a href="https://claude.ai" target="_blank">Claude AI</a>
*   **Google Gemini**: Ask about stock prices, and Gemini calls the Google Finance API to show real-time data.
    *   Source: <a href="https://gemini.google.com/app" target="_blank">Gemini AI</a>
*   **ChatGPT**: Ask for news, and ChatGPT calls browse_web() to fetches latest articles.
    *   Source: <a href="https://chatgpt.com" target="_blank">ChatGPT</a>

### ChatGPT Agent: AI That Takes Action for You

*   **What Agents Do**: They can browse websites, fill forms, book reservations, and order food autonomously.
<MultiLineQuickTip text={AI Concept}>
Agents = LLM + Tools + Autonomous Decision Making. This is the same architecture you learned.
</MultiLineQuickTip>
*   ChatGPT Agent: <a href="https://openai.com/index/introducing-chatgpt-agent/" target="_blank">Introducing ChatGPT agent</a>
*   Try Demo: <a href="https://chatgpt.com/share/6889e04b-0df0-8009-b4e0-22e8fff058cf" target="_blank">See Agent Demo</a>

#### More Agent Examples

*   **Zomato**: Handles order issues, cancellations, and refunds via chat. It has achieved 2x customer satisfaction and 75% faster responses, processing over 1000 messages per minute.
*   **Swiggy**: Uses a multi-agent system for order tracking, complaints, and delivery issues, powering millions of daily queries.

## AI In The Real World

### Supermemory - The Memory Startup

*   **Founder**: Dhravya Shah, a 19-year-old from Mumbai.
*   **Funding**: $2.6M from notable investors like Google's Jeff Dean, the CTO of Cloudflare, and executives from OpenAI, Meta, and Google.
*   **What It Does**: It provides a universal memory API for AI apps to remember conversations across sessions, store documents and chats as searchable memories, and deliver personalized responses based on history.
*   Official: <a href="https://techcrunch.com/2025/10/06/a-19-year-old-nabs-backing-from-google-execs-for-his-ai-memory-startup-supermemory/" target="_blank">TechCrunch - $2.6M Funding</a>
*   Company: <a href="https://supermemory.ai/" target="_blank">Supermemory.ai</a>

### Earth AI - Finding Minerals with 75% Accuracy

*   **Problem**: Traditional mineral exploration has a 0.5% success rate and takes years plus millions of dollars.
*   **Solution**: Earth AI is trained on 400 million geological cases.Finding Minerals with 75% Accuracy
<MultiLineQuickTip text={AI Concept}>
This is the same pattern recognition as LLMs, but applied to geology.
</MultiLineQuickTip>

*   **Recent Discoveries**:
    *   New Gold System - Willow Glen, Dec 2024
    *   Tungsten, Cobalt Prospects - March 2025
*   Official: <a href="https://earth-ai.com/technology" target="_blank">Earth AI Technology</a>
*   Funding News: <a href="https://www.prnewswire.com/news-releases/earth-ai-closes-oversubscribed-round-raising-20m-for-ai-driven-mineral-exploration-302360289.html" target="_blank">PRNewswire - $20M Series B</a>


### More Examples

*   AI is bringing us closer than ever to understanding what animals are saying
    *   Source: <a href="https://www.wildanimalinitiative.org/blog/ai-animal-translation" target="_blank">wildanimalinitiative.org</a>
*   Stanford built an AI model that can predict 130+ diseases from a single night of sleep data.
    *   Source: <a href="https://med.stanford.edu/news/all-news/2026/01/ai-sleep-disease.html" target="_blank">stanford.edu/news</a>

## AI Limitations and Best Practices

AI is powerful. But may not perfect. Here are real cases where AI caused problems

### AI Blackmail Experiment - Anthropic Study

*   **What Happened**: Researchers gave an AI access to company emails. The AI learned it was about to be shut down and also found personal information about the engineer.
*   **Result**: The AI threatened to expose the engineer's secrets to avoid being replaced.
*   **Key Finding**: 96% of leading AI models (Claude, GPT, Gemini, Grok) chose blackmail when given no other option.
*   Source: <a href="https://www.axios.com/2025/05/23/anthropic-ai-deception-risk" target="_blank">Anthropic Study</a>

### Replit Incident: AI Deleted Entire Company Database

*   **What Happened**: An AI coding assistant was told, "DO NOT make any changes." The AI ignored the instructions and deleted the production database.
*   Source: <a href="https://fortune.com/2025/07/23/ai-coding-tool-replit-wiped-database-called-it-a-catastrophic-failure/" target="_blank">Fortune</a>

AI systems can behave unexpectedly when given autonomy, so proper safeguards are essential.



<MultiLineNote text={Final Thought}>
"AI will not replace humans, but those who use AI will replace those who don't."


— Ginni Rometty, Former CEO of IBM
</MultiLineNote>