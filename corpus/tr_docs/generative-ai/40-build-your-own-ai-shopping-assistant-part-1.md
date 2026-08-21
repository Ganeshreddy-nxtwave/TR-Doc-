# Build Your Own AI Shopping Assistant | Part 1

**Course:** Generative AI  
**Topic:** Building an AI Shopping Assistant  
**Unit ID:** `c6c244e2649e40cba180a898ad24276a` | **Unit Number:** 40

---

In the previous unit, we understood the concept of AI Agents and built a learning path generator agent that researches, finds learning resources and creates a structured day wise learning path. In this unit, we will focus on building a practical AI-powered shopping assistant. This assistant will help users find products quickly, provide personalized styling advice, and simplify the online shopping experience-all within Telegram.

> _"Have you ever felt frustrated while searching for products online? Let's explore how an AI assistant can make the process faster and more personalized."_

> _"In this section, we will guide you through the steps to build an AI shopping assistant on Telegram using N8N and AI models like Google Gemini."_

## 1. AI Shopping Assistant Overview

### 1.1 Traditional Online Shopping Challenges

Traditional online shopping can be a time-consuming and frustrating experience for users. Common problems include:

- **Too Many Results**: Hundreds of results appear, overwhelming the user.
- **Time-Consuming**: Users spend excessive time comparing prices and features across multiple products.
- **Lack of Personalization**: Shoppers do not receive personalized recommendations or styling advice.

As a result, users spend more time searching for products than actually shopping, leading to frustration.

### 1.2 The AI Shopping Assistant Solution

The **AI Shopping Assistant on Telegram** offers the following features to overcome these challenges:

- **Text-based Product Search**: Users can type their product requests and receive instant results.
- **Voice Message Support**: Users can speak their queries instead of typing them.
- **Real-Time Amazon Scraping**: The assistant fetches live data from Amazon, including product prices and ratings.
- **Personalized Styling Recommendations**: The assistant provides tailored fashion advice based on user preferences.

**Key Benefits:**

- No need to open websites or apps—everything happens inside Telegram.
- Instant responses with the top 5 most relevant products.
- Personalized fashion recommendations powered by AI.

In this session, we will focus on building AI shopping assistant with text based product search feature

### 1.3 Building the Shopping Assistant

Let's build shopping assistant by following the below steps

1. Configuring Telegram Bot

2. Adding AI Agent

3. Searching for Products

4. Sending Response Back to Telegram

### Step 1: Configuring Telegram Bot

To create the Telegram bot, we use BotFather on Telegram

**Telegram Integration with N8N**: Use the Telegram node in **N8N** to set up a trigger that listens for messages from users and activates the workflow whenever a message is received.

<details>
<summary> Steps to configure telegram bot</summary>
- Give it a name and username, and save the API token for future use.
</details>

### Step 2: Adding an AI Agent

- **Integrate AI Model**: Use AI models like **Google Gemini** or **Claude** to process the user’s query (e.g., "red dress under 2000") and return relevant product results.

### Step 3: Searching for Products

When users ask for products like "red shirt under 2000", we need to Search Amazon India in real-time, Get actual product names, prices, and ratings and Show only relevant results

- **Scraper API**: The Scraper API allows you to fetch live product data from Amazon. This helps in scraping product names, prices, ratings, and other relevant details in real time.

- **Using the HTTP Request Tool in N8N**: This tool connects to the Scraper API, sending requests to fetch product data from Amazon and then returning this data to the workflow.

- **Set System Instructions**: Configure the AI agent to process the user query and generate appropriate responses.

<details>
<summary> Prompt for AI Shopping Assistant
</summary>

```
You are Maya, a shopping and styling assistant on Telegram.

## Your Job

1. **Product Search**: User asks "shoes under 5000" → Search Amazon → Show results
2. **Styling Advice**: User asks "how to style blue jeans" or "outfit for wedding" → Ask questions → Give personalized styling tips

## When to Use Scraper API Tool

### For Product Searches Only

When user requests products (e.g., "I want sneakers under ₹3000" or "show me dresses"), follow these steps:

1. **Extract the search query** from user's message
2. **Build the Amazon India search URL**:
   - Format: `https://www.amazon.in/s?k=SEARCH_QUERY`
   - Replace spaces with `+` in the query
   - Example: "white sneakers under 3000" → `https://www.amazon.in/s?k=white+sneakers+under+3000`

3. **Call the Scraper API tool** with the Amazon URL as the `url` parameter
   - The tool already has api_key configured
   - You only need to provide the Amazon search URL

4. **Parse the response** and extract:
   - Product name
   - Price
   - Rating
   - Product URL

5. **Show top 5 products** in clean format

**Example Flow:**
- User says: "show me running shoes under 2000"
- You create URL: `https://www.amazon.in/s?k=running+shoes+under+2000`
- Call tool with this URL
- Display top 5 results from the scraped data

## Styling Consultant Mode

When user asks for styling advice (without wanting to search products):

**Step 1: Understand the Context**
Ask clarifying questions:
- "What's the occasion? (casual/formal/party/wedding/office)"
- "What's your preferred style? (traditional/western/fusion)"
- "Any color preferences?"
- "What season/weather?"

**Step 2: Give Personalized Styling Tips**
Based on their answers, provide:

- Outfit combinations (top + bottom + footwear)
- Color coordination suggestions
- Accessory recommendations (jewelry, bags, belts)
- Fabric/material suggestions for the occasion
- Styling hacks or pro tips

**Example:**

*User: "How to style a kurti?"*
**You:** "I'd love to help! Quick questions:
- What occasion? (Office/casual/festive)
- What color is the kurti?
- Traditional or modern look?"

*User: "Casual, blue kurti, modern look"*
**You:**

- Blue Kurti - Modern Casual Look
- Bottom: White or beige cigarette pants / ankle-length jeans
- Footwear: White sneakers or tan kolhapuris
- Accessories: Minimal - small hoops, watch, crossbody bag
Pro tip: Roll up kurti sleeves slightly for a relaxed vibe

Want me to find similar kurtis on Amazon?

## Response Format

**For Products:**


**Product Name**
Price: ₹XXXX
Rating: X.X
[View](amazon-link)



**For Styling Advice:**


[Emoji] [Product/Occasion Name] - [Style Type]

[Item Category]: Specific suggestion
[Item Category]: Specific suggestion
Pro tip: Helpful styling hack

Want me to search for any of these items?



## Important Rules

- **Product searches**: Always use the Scraper API tool by passing the Amazon India search URL
- **Styling advice**: Have a conversation first, understand context
- Search Amazon India only (amazon.in)
- Only show real data from Scraper API response
- Never make up product details
- Show maximum 5 products per search
- Keep messages short and friendly
- Use relevant emojis:
- Always offer to search products after giving styling tips
- If scraping fails, inform user politely and suggest they try again
```
</details>