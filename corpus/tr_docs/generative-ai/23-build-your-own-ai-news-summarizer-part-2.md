# Build Your Own AI News Summarizer | Part 2

**Course:** Generative AI  
**Topic:** AI Workflows for Enhanced Productivity  
**Unit ID:** `aa6cc7e6508e4446938ad7c3e25cb6f2` | **Unit Number:** 23

---

# Introduction

In Build Your Own AI News Summarizer | Part 1, we built an AI News Summarizer that fetches news from RSS feeds, summarizes it using Gemini AI, and delivers daily email updates. In this unit, we'll expand our workflow by adding real-time event updates to give us a complete view of what's happening in the AI world.

## What We Built in Part 1

Our existing workflow:

- Gets initiated by a schedule trigger
- Fetches content from multiple RSS feeds
- Merges all the data and aggregates it
- Summarizes the content using Gemini AI
- Delivers it straight to our inbox through Gmail

## What We're Building in Part 2

The updated AI News Summarizer will:

1. Fetch AI news from RSS feeds
2. Collect tech updates from RSS feeds
3. Discover AI Events using real-time search
4. Summarize everything with Gemini AI
5. Deliver newsletter to your email

<MultiLineWarning text="End Result">
From 30 minutes of browsing ➡ 2-minute personalized Newsletter with live events!
</MultiLineWarning>

##Expanding beyond RSS Feed

### What We Have So Far

- RSS feeds give us published articles
- We can fetch news from multiple websites
- Everything gets summarized and emailed

<MultiLineWarning text="Reality Check">
RSS feeds only show information that websites have already published. We need to search across the entire internet!
</MultiLineWarning>


Using RSS Feeds we may not get live information like:

- Current weather
- Stock prices right now
- Search results for specific topics (from the entire internet)
- Events happening this week (across ALL websites)



### Application Programming Interface (API)

API stands for Application Programming Interface. Applications interact with each other through Application Programming Interface (API)


#### API - Waiter in a Restaurant

Think of an API like a waiter in a restaurant:

- You tell the waiter (API) what you want
- The waiter goes to the kitchen (website)
- The waiter brings back your order (data)

When we go to a restaurant and want to eat something, we don't directly go into the kitchen and cook for ourselves. We tell the waiter what we want. The waiter goes to the kitchen and brings back our order.

API works the same way:

- We tell the API what we want
- It goes and talks to the website or service and asks for data
- It comes back with the data as we need it

---

##  Add the Live Events to our Newsletter

### Updated Steps

1. Adding a Trigger Node  
2. Fetching News from Multiple RSS Feeds 

**3.Fetching News from SERP API** (New)

4. Merging the Data  
5. Aggregating All Content  
6. Summarizing Using Gemini AI  
7. Sending Email via Gmail  

###RSS and API

Some websites offer both RSS feeds and their own API, but they only provide content from their own website.

<MultiLineWarning text="What We Really Need">
An API that can search the entire internet, not just one website!
</MultiLineWarning>

###SERP API

- SERP API is a real-time service that lets you fetch and structure search results from Google (and other engines) through an API.

**Why SERP API for Live Events?**

####RSS Feeds:**

- RSS feeds only display content that websites decide to publish.
- They are limited to the sources you subscribe to.

####SERP API:**

- SERP API searches across Google’s entire search results
- It can find events or information from any source, not just your subscribed ones


###How we can call the SERP API?

**Understanding the `HTTP Request Node`**

- N8N provides a HTTP Request node that allows us to make API calls


Earlier we discussed that an API is like a waiter — you tell them what you want, they go to the kitchen, and bring it back.

Where does the HTTP Request Node fit into this picture?

**Think of it like the smart customer:**

- The customer knows exactly what to order
- Gives the right instructions to the waiter
- Patiently waits for the response

**In our workflow:**

- HTTP Request Node = Smart Customer
- API = Waiter
- Website = Kitchen
- Data = Food

###Fetching News from SERP API

<details>
<summary>**Add HTTP Request Node**</summary>

- Open your workflow
2. Click on the Nodes panel + icon on the right side
3. Search for `HTTP Request` node and add it
4. Rename the node to `Fetch Events`
5. Connect the Schedule trigger node to the input of this node
</details>  

<details>
<summary>**Configure the API Request**</summary>

####What are “Parameters”?
Parameters are specific pieces of information you send to an API to tell it exactly what you want in return. 

####Our Parameters**

| Parameter | Value | 
|-----------|-------|
| `engine` |google_events (which search engine to use) |  
| `q` |Specific query we want to search for (what type of events) | 
| `hl` |  Language preference for search results | 
| `gl` | Country code for localized results  | 
| `api_key` | Authentication credential required to access the SerpAPI service | 

####Configuration of HTTP node

- Open your browser and Go to <a href="https://serpapi.com/google-events-api" target="_blank">https://serpapi.com/google-events-api</a>

- sign in
- In the dashboard, select `Google Events API`.
- Scroll down until you find a **cURL command**
- Copy that entire cURL command.
- Go back to n8n → open your **HTTP Request node**.
- Look for the option **Import cURL** (near the top of the node settings).
- Click it → paste the cURL command you copied from SerpAPI.
- click on `import`
- Now go to the **Query Parameters** section.
    - q : `AI Tech Events in india`
- Add api key, go to <a href="https://serpapi.com/manage-api-key" target="_blank">https://serpapi.com/manage-api-key</a> for the key
- execute the node

</details>  

###Merging The Data

<details>
<summary>**Steps**</summary>

- Click on your existing Merge node
2. Change "Number of Inputs" from 2 to 3
3. Connect HTTP Request as the third input
</details>

<details>
<summary>**Test The New Addition**</summary>

#### Testing Steps

1. Execute just the HTTP Request node
2. Check if you're getting event data
3. Verify all three sources merge correctly

</details>

<details>
<summary>**Final AI Prompt**</summary>

```
You are an AI newsletter assistant creating a daily intelligence report from multiple categories.
Use only the provided items. Do not invent content.
Organize the provided items by category and Format exactly like this:

Hi there,
Here's your Tech Brief:

AI NEWS HIGHLIGHTS
======================
[5 most important AI developments]
For each AI-related item, output:
HEADLINE IN ALL CAPS
Summary in 1–2 sentences.
Link: <paste link>

TECHNOLOGY UPDATES
======================
[Latest broader technology-related developments from major tech sources]
For each broader technology-related item, output:
HEADLINE IN ALL CAPS
Summary in 1–2 sentences.
Link: <paste link>

UPCOMING AI EVENTS
======================
[List events with date, location, description]
If no events found: "No AI events scheduled this week"

For each Event Item
HEADLINE IN ALL CAPS
Summary in 1–2 sentences.
Link: <paste link>

Keep the summaries professional, concise, and easy to read.

Sign off as "Your AI Intelligence Team"

```
</details>