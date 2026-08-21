# Build Your Own AI News Summarizer | Part 1

**Course:** Generative AI  
**Topic:** AI Workflows for Enhanced Productivity  
**Unit ID:** `0f2a4f26c7ff424ea6988a72c0ce54bf` | **Unit Number:** 21

---

# Introduction

In the previous unit, we built an AI-Powered Social Media Content Creator & Publisher that automated article listing, summarization, and posting using n8n. In this unit, we’ll focus on building our own AI News Summarizer — a personal assistant that fetches news from RSS feeds, summarizes it, and delivers a daily email update.

## Build Your Own AI News Summarizer

### The Daily Struggle
Every morning, many professionals face the same challenge when trying to stay updated with technology news. The typical routine involves:

- Opening 10+ different tech websites
- Scrolling through hundreds of articles
- Trying to filter what's actually important
- Struggling to remember key points throughout the day

This process typically consumes 30-45 minutes each morning, which could be better utilized for productive work.

<MultiLineWarning text="Solution">
Instead of spending half an hour browsing multiple websites, imagine receiving a perfectly summarized email at 10 AM with only the most relevant AI news.
</MultiLineWarning>

## What We're Building

The AI News Summarizer is an automated system that:

-  Fetches AI news from multiple sources
2. Collects tech updates automatically
3. Summarizes content using Gemini AI
4. Delivers a newsletter directly to your email

<MultiLineWarning text="End result">
From 30 minutes of browsing ➡ 2-minute personalized Newsletter!
</MultiLineWarning>

### Prerequisites

Before building the system, you'll need:

- n8n Account
- Google Account
- RSS Feed URLs

##How can we Fetch the Latest News?

### RSS Feed

- RSS is like a news delivery system. 
- Instead of you visiting many websites, the updates come directly to you. 
- Think of it like subscribing to a newspaper, but online.

**Finding RSS Feeds**

There are several ways to locate RSS feeds:

- Look for the `RSS icon at the bottom of websites`
    - <a href="https://www.theverge.com/24036427/rss-feed-reader-best" target="_blank">https://www.theverge.com/24036427/rss-feed-reader-best</a>
    - <a href="https://thehackernews.com/" target="_blank">https://thehackernews.com/</a>


2. Try `adding /rss` or `/feed` at the end of a website's URL
    - <a href="https://www.reddit.com/r/technology/.rss" target="_blank">https://www.reddit.com/r/technology/.rss</a>
    - <a href="https://techcrunch.com/category/artificial-intelligence/feed/" target="_blank">https://techcrunch.com/category/artificial-intelligence/feed/</a>

- Some websites provide ready-to-use RSS feeds
- We can use these feeds directly when needed
- Example:
    - Website - <a href="https://aibusiness.com/" target="_blank">https://aibusiness.com/</a>
    - RSS Feed URL - <a href="https://aibusiness.com/rss.xml" target="_blank">https://aibusiness.com/rss.xml</a>
- With this RSS Feed URLs, we can get the latest articles, posts, or news published on that website
- However, the actual coverage depends on the website's configuration and choices

- You can follow these to get latest rss feeds from:
    - <a href="https://github.com/foorilla/allainews_sources" target="_blank">https://github.com/foorilla/allainews_sources</a>
    - <a href="https://github.com/vishalshar/awesome_ML_AI_RSS_feed" target="_blank">https://github.com/vishalshar/awesome_ML_AI_RSS_feed</a>
    - <a href="https://github.com/RSS-Renaissance/awesome-AI-feeds" target="_blank">https://github.com/RSS-Renaissance/awesome-AI-feeds</a>

##Let's build a workflow for Fetching RSS News and Sending Summarized Emails

###Steps to Follow
<details>
<summary>**Adding a Trigger Node**</summary>
- Let's say we want to receive news updates everyday at 10:00 AM

####How can we schedule it?
- A special node in n8n that automatically starts your workflow at specific times
    - Wakes up your automation exactly when you want
    - No manual clicking – runs in background


#### Why Schedule Trigger?
- Instead of manually running your news summarizer every morning, the Schedule Trigger does it for you
- You can set it to run at any time - daily, weekly, or even multiple times a day
- Perfect for routine tasks like fetching morning news at 10 AM every day

#### Adding a Schedule Trigger:
A Schedule Trigger is a special node in n8n that automatically starts your workflow at specific times. It requires no manual clicking and runs in the background, waking up your automation exactly when you want.

**Configuration Steps:**
1. Position at start of workflow
2. Add Schedule Trigger node
3. Set interval to "Every Day"
4. Configure trigger time to "10:00 AM"

</details>

<details>
<summary>**Fetching News from RSS Feeds**</summary>

#### RSS Feed Read Node

The RSS Feed Read Node in n8n serves three main purposes:

- Fetches the latest updates from any RSS feed URL
- Automatically retrieves new articles since last check
- Processes the feed data into a usable format

**Fetching News from RSS Feeds:**
1. Connect RSS Read node to Schedule Trigger
2. Paste RSS Feed URL (e.g., <a href="https://aibusiness.com/rss.xml" target="_blank">https://aibusiness.com/rss.xml</a>)
3. Execute to test the connection

</details>

<details>
<summary>**Aggregating All Content**</summary>
<br>
Sometimes you have separate pieces of data from the RSS feed. The Aggregate node bundles them together, and the result is a single piece of data.

**Configuration:**

- Add Aggregate node after RSS Feed Read
2. Set to "Aggregate All Item Data"
3. This creates a single JSON object with all articles

</details>

<details>
<summary>**Summarizing Using Gemini AI**</summary>
<br>
#### Gemini AI Model Setup

- Add Basic LLM Chain Node
- Then Search and Add Google Gemini Chat Model
- Choose gemini-2.5-flash model 

<details>
<summary>Configure with this Prompt</summary>

```
You are an AI news summarizer assistant.
Analyze the news articles and create an email summary.

For each article:
Create a headline in ALL CAPS
Write a 2-3 sentence summary
Include the article link

Format as:
Subject: Today's AI News

Hi there,

Here's your AI news summary:

HEADLINE IN CAPS
Summary of what happened and why it matters...
Read more: [link]

Best regards,
AI News Bot

```
</details>

</details>

<details>
<summary>**Sending Email**</summary>

#### Step 1: Create a Gmail Send Node
- Open your n8n workflow.  
- Click `+` to add a new node.  
- Search for `Gmail → Send a message`.  
- Click `Create New Credential` → Select `OAuth2 authentication`.

---

#### Step 2: Enable Required APIs
- Go to `APIs & Services → Library` in the Google Cloud Console.  
- Search for the required API (e.g., `Gmail`, `Sheets`, `Drive`, `Calendar`).  
- Select `Gmail API`.  
- Click `Enable`.

---

#### Step 3: Configure OAuth Consent Screen
- Go to `APIs & Services → OAuth consent screen`.  
- Click `Get started`.  
- Fill in the following details:
  - `App name:` AI-news-summarizer  
  - `User support email:` your email address  
  - `Audience:` select `External`  
  - `Developer contact information:` same email as above  
- Read and accept Google’s User Data Policy.  
- Click `Create`.

##### Configure Branding and Domains
- From the left menu, select `Branding`.  
- In `Authorized domains`, click `Add domain`.  
- Add the domain: `earlywave.in`.  
- Click `Save`.

---

#### Step 4: Create OAuth 2.0 Credentials
- Navigate to `APIs & Services → Credentials`.  
- Click `Create Credentials → OAuth client ID`.  
- Select `Web application` as the application type.  
- Set `Name:` n8n-AI-news-summarizer.  
- Copy the OAuth Redirect URL from the n8n workflow and paste it under `Authorized redirect URIs`.  
- Click `Create`.  
- Copy the `Client ID` and `Client Secret`.  
- Paste them in the corresponding fields inside the n8n workflow.  
- Click `Save` in n8n.  
- Click `OK` in Google Cloud Console.

---

#### Step 5: Publish the App
- Go to `APIs & Services → OAuth consent screen`.  
- Navigate to the `Audience` section.  
- Under `Publishing status`, click `Publish App`.  
- Confirm the publication.

---

#### Step 6: Gmail Send Node Integration (n8n)
- Open the `Gmail Send` node in the n8n workflow.  
- Click `Sign in with Google`.  
- Select the Gmail account.  
- On the security warning screen, click `Advanced → Go to earlywave (unsafe)`.  
- Review and grant the requested permissions.  
- Click `Continue / Allow`.  
- Click `Save` to store the credential.

---

#### Step 7: Configure Recipient Details (n8n)
- In the same Gmail node:
  - Set the `To` field with the recipient’s email address.  
  - Set `Subject:` Today's AI News for you...  
  - Set `Email Type:` Text  
  - In the `Message` field, insert:  
    ```
    {{ $json.text }}
    ```

</details>

### Adding Multiple News Categories
<MultiLineWarning text="Question">
What if we want technology news along with AI news?

</MultiLineWarning>

<MultiLineWarning text="Solution">
So far, we have been fetching AI news from one RSS feed. Now, let's learn how to add technology news from another RSS feed to get a complete view of the news

</MultiLineWarning>


### Updated Workflow Steps
1. Adding a Trigger Node (already completed)

<details>
<summary>**2.Fetching News from Multiple RSS Feeds**</summary>

#### Add RSS Read Node for Technology Updates

- Click on the end of the `Schedule Trigger` node.  
- Add another node and select `RSS Read`.  
- Name the node as `Technology Updates Feed`.  
- Set the `Feed URL` to:  <a href="https://techcrunch.com/feed/" target="_blank">https://techcrunch.com/feed/</a>
- Execute the node to fetch the latest news.

</details>


<details>
<summary>**3.Merging the Data**</summary>


### Understanding the Merge vs Aggregate Difference
**n8n Merge Node**

- Data can come from multiple sources
- The Merge node combines them into one output stream
- Each piece of data still remains separate


<MultiLineWarning text= "Merge vs Aggregate">
**Merge** is like collecting papers from different files into one stack (still separate sheets)
But **Aggregate** is like stapling all those sheets together into one document

</MultiLineWarning>
#### What Merge Does?

- Collects items from different sources
- Puts them in one place
- Each item stays separate
- Like collecting papers from different files into one stack (still separate sheets)

#### What Aggregate Does?

- Takes all separate items
- Combines them into one unit
- Creates a single document
- Like stapling all those sheets together into one document


### Merge Configuration

-  Add Merge node
2. Set "Number of Inputs" to 2
3. Connect both RSS nodes to Merge inputs
4. This combines articles from both sources

<details>
<summary>Updating the AI Prompt</summary>

```
You are an AI news summarizer handling multiple categories.
Use only the provided items. Do not invent content.

Organize by category and provide up to 3 AI news and up to 3 broader technology news.

Format exactly like this:

Hi there,
Here's your Tech Brief:

AI NEWS
=======
For each AI-related item, output:
HEADLINE IN ALL CAPS
Summary in 1–2 sentences.
Link: <paste link>

TECHNOLOGY UPDATES
==================
For each broader technology-related item, output:
HEADLINE IN ALL CAPS
Summary in 1–2 sentences.
Link: <paste link>

Keep it professional, concise, and easy to read.

```


</details>

</details>


4. Aggregating All Content
5. Summarizing Using Gemini AI
6. Sending Email via Gmail


## Testing and Deployment

### Testing Your Complete Workflow

Schedule Trigger → Parallel RSS Fetching → Merge → Aggregate → AI Summary → Gmail

### Test Checklist
1. Click "Execute Workflow" for manual test
2. Verify each node processes correctly
3. Check email formatting
4. Activate for daily automation
## Key Benefits

### What You've Built
- Automated news monitoring from multiple sources
- AI-powered summarization
- Daily email delivery at 10 AM
- 30+ minutes saved every day