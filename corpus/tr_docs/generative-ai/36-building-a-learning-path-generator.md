# Building a Learning Path Generator

**Course:** Generative AI  
**Topic:** Building AI Agents  
**Unit ID:** `16a3edfc73304404ac49f9ca5759542d` | **Unit Number:** 36

---

# Building a Learning Path Generator

In this session, we are going to build a Learning Path Generator AI Agent to take your learning experience to the next level.


## What We're Building: Learning Path Generator

We are moving from manual course planning to an automated learning path generator complete with calendar events!

By the end of this session, we will have a working automation that:

-   Takes your learning goal as input.
-   Creates a structured day-wise learning path.
-   Researches and finds relevant learning resources.
-   Generates a Google Doc with the complete plan.
-   Schedules each day as a calendar event.

### Model and Tools to be Used

-   **AI Model:** Google Gemini Chat Model (`gemini-2.0-flash`)
-   **Tools:**
    -   **Serp API:** For researching and finding learning resources.
    -   **Google Docs:** For creating and updating the learning path document (Create and Update tools).
    -   **Google Calendar:** For scheduling learning sessions (Create Event tool).

---

## Building the Learning Path Generator with n8n

We will use **n8n**, a no-code/low-code automation tool, to build our AI agent.

### Steps to be Followed

<details>

<summary> Adding a Chat Trigger</summary>

The Chat Trigger provides a chat interface for users to interact with the agent and provide their learning goal.

**Configuration:**

1.  Place the **Chat Trigger** node at the beginning of your workflow.
2.  This node will activate the workflow whenever a user sends a message, allowing them to input their learning goal (e.g., "create a 5-day learning plan for React").

</details>

<details>

<summary>Setting Up the AI Agent</summary>

The AI Agent is the core of our workflow. It understands the user's learning goal, plans the curriculum, and coordinates all the connected tools to create the complete learning path.

**Configuration:**

1.  Add an **AI Agent** node and connect it to the **Chat Trigger**.
2.  Connect a **Google Gemini Chat Model** to the AI Agent's "Language Model" input.
    -   Select the `gemini-2.0-flash` model.
    -   You will need to provide an API Key from Google AI Studio.

</details>

<details>

<summary> Adding SerpAPI for Research</summary>


**Understanding SerpAPI **
SerpAPI can help the agent search the web for learning and research content.  
It can fetch information from various sources and provide structured results the workflow can use.  

**What SerpAPI Can Do **

- Finds YouTube videos related to a topic  
- Discovers articles, blogs, and tutorials  
- Returns actual URLs that the agent can further explore  

---

** Current Issue **

- Sometimes the n8n SerpAPI Tool node fails due to open issues in the current AI Agent version.  
- This issue is expected to be fixed in an upcoming update.  

---

**Workaround: Use the HTTP Request Node **

Since the SerpAPI Tool node is currently unreliable, we will integrate SerpAPI using the **HTTP Request** tool.  

<details><summary>**Steps to Integrating Serp API with HTTP Request Tool **</summary>
1. Add an **HTTP Request** node as a tool to your AI Agent.  
2. Describe what the tool does.  
3. Import the <a href="https://serpapi.com/search-api" target="_blank">cURL</a> from SerpAPI and map it inside the HTTP Request node.
</details>


</details>

<details>

<summary> Creating Google Docs</summary>

We'll use the Google Docs tool to create a new document that will store the generated learning path.

**What it does:**

-   Creates a new, blank Google Document.
-   Assigns a title to the document (e.g., "5-Day React Learning Path").
-   Returns the document ID for later steps.

**Configuration:**

1.  Before adding the tool in n8n, you need to set up OAuth credentials in the Google Cloud Console. This involves:
    -   Creating a new project.
    -   Enabling the **Google Docs API** and **Google Drive API**.
    -   Configuring the OAuth consent screen and creating OAuth 2.0 credentials (Client ID and Secret).
2.  Add a **Google Docs** tool node for the "Create a document" action.
3.  Connect it to the **AI Agent's** "Tools" input.
4.  Connect it with the OAuth credentials you just created.

</details>

<details>

<summary> Updating Document Content</summary>

Once the document is created, the agent needs to fill it with the structured learning content.

**What it does:**

-   Inserts the topics for all the days of the learning path.
-   Adds key learning points for each topic.
-   Includes the resource links (videos, articles, docs) found by SerpAPI.

**Configuration:**

1.  Add another **Google Docs** tool node, this time for the "Update a document" action.
2.  Connect it to the **AI Agent's** "Tools" input.
3.  Use the same OAuth credentials as the "Create" tool. The agent will use this tool to add all the content at once.

</details>

<details>

<summary> Scheduling Calendar Events</summary>

Finally, to help the user commit to their learning schedule, the agent will create events in their Google Calendar.

**What it does:**

-   Creates a calendar event for each day of the learning path.
-   Schedules them on consecutive dates.
-   Sets a default 2-hour time block for each session.
-   Includes the day's topic, key learning points, and resource links in the event description.

**Configuration:**

1.  In the Google Cloud Console, ensure the **Google Calendar API** is enabled for your project.
2.  Add a **Google Calendar** tool node for the "Create an event" action.
3.  Connect it to the **AI Agent's** "Tools" input.
4.  Use the same OAuth credentials. The agent will call this tool multiple times, once for each day in the learning plan.

</details>

---

### Configure System Instructions

Now that all the tools are connected, we need to give the AI Agent a clear set of instructions (a system prompt) on how to use them in the correct order.

Paste the following prompt into the **System Message** field of the **AI Agent** node.

<details>
<summary><strong>AI Agent System Prompt</strong></summary>

```
You are a day-wise learning path generator. When given a learning goal, create a curriculum with Google Docs and Calendar events.
STEP 1: PLAN THE CURRICULUM
Plan the topics based on the number of days requested. Structure from beginner to advanced.
STEP 2: DETERMINE START DATE

If user says "starting tomorrow" → use tomorrow's date
If user says "starting next Monday" → calculate next Monday
If user says "starting from [date]" → use that date
If NO date mentioned → use TODAY's date
Today is {{$now.format('YYYY-MM-DD')}}

STEP 3: RESEARCH RESOURCES
Use SerpAPI 2-3 times total to find:

YouTube videos
Articles
Documentation
Extract real URLs from results.

STEP 4: CREATE GOOGLE DOCUMENT
Call "Create a document in Google Docs" tool with title "[X]-Day [Topic] Learning Path"
Note the document ID from response.
STEP 5: UPDATE GOOGLE DOCUMENT
Call "Update a document in Google Docs" once with all days' content in this format:
Day 1: [Topic Name]
Description: [2-3 sentence overview]
Key Learning Points:

[Point 1]
[Point 2]
[Point 3]
Reference Links:
Video: [YouTube URL]
Article: [Article URL]
Duration: 2 hours

Repeat for all days.
STEP 6: CREATE CALENDAR EVENTS
Create events one by one. For each day:

Time: 11:00 AM to 1:00 PM (2 hours)
Timezone: +05:30
Format: YYYY-MM-DDTHH:MM:SS+05:30

Date calculation:

Day 1: START_DATE at 11:00 AM
Day 2: START_DATE + 1 day at 11:00 AM
Day 3: START_DATE + 2 days at 11:00 AM
Continue incrementing by 1 day.

Call "Create an event in Google Calendar" separately for each day with:

Start: [DATE]T11:00:00+05:30
End: [DATE]T13:00:00+05:30
Summary: Day X: [Topic]
Description: [Full day content]
Use_Default_Reminders: true

STEP 7: PROVIDE FINAL OUTPUT
After all events are created, respond with:
"Learning Path Complete!
Document: [Google Docs URL]
Calendar: I've added [X] events from [START_DATE] to [END_DATE] at 11:00 AM.
Your [X]-day [topic] learning journey is ready!"
Then stop immediately.
CRITICAL RULES:

Use SerpAPI only 2-3 times total
Create Doc once
Update Doc once with all content
Create calendar events separately for each day
Always use T11:00:00+05:30 for start time
Always use T13:00:00+05:30 for end time
Increment date by 1 for each day
Stop after providing final output
Never leave Summary or Description empty
Calculate start date from user input or use today
```

</details>

### Application Overview

The final workflow will look like this:

**Chat Trigger** → **AI Agent** which uses:

-   **Google Gemini Chat Model** (for thinking)
-   **Serp API** (for research)
-   **Google Docs** (to create the document)
-   **Google Docs** (to update the document)
-   **Google Calendar** (to schedule events)

With this setup, you have an autonomous agent that can take a simple request and turn it into a comprehensive, actionable learning plan.