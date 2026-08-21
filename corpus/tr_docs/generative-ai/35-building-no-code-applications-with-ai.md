# Building No-Code Applications with AI

**Course:** Generative AI  
**Topic:** Mastering Audio Generation & No-Code Application Building  
**Unit ID:** `f3eaf09367694889bbc09c2aefe8284c` | **Unit Number:** 35

---

# Introduction

In the previous unit, we built an AI Podcast Generator that automated audio content creation using n8n and Murf.ai. In this unit, we'll focus on transforming our workflow into a real web application — a user-friendly interface that anyone can access and use without knowing anything about n8n or automation.

## Build Your Own No-Code Application

**The Challenge**

Our n8n workflows are powerful but hidden

- They run automatically inside n8n
- Only the workflow creator can see and use them
- Others can’t use them like regular apps

What if others could use our workflows like normal apps?

> **Solution**
> 
> No-Code Application Building

###What to Achieve?

We will be building a frontend application for our Podcast Generator workflow

- The Complete Flow

    - User clicks `Generate Podcast`
    2. Trigger n8n Workflow
    3. n8n processes request (Generate content & convert to audio)
    4. Send results back to UI
    5. UI displays or plays podcast


###No-Code Application Building

You might have built applications using:

- Lovable
- Bolt
- And other no-code tools
complete applications in just minutes!


###Vibe Coding

- Vibe Coding is a new way to build interfaces
- You simply describe what you want in natural language
- AI generates the complete interface for you
- Think of it like telling a designer your vision and watching it come to life

###Meet the AI Application Builders

There are 100s of tools like: 

- Replit
- Lovable 
- Base44, Claude Artifacts, V0 by Vercel, and Bolt 

---

##Building a Podcast Generator

### What We're Building

- **Frontend** : Create a beautiful interface first
- **N8n Workflow**: Update our workflow to accept requests
- **Connection**: Link them seamlessly together

###Steps to Follow

<details>
<summary>**Creating a Beautiful Frontend**</summary>
<br>

<b>Open Lovable Platform</b>

- Go to lovable.dev
- Login to the website
- Paste the prompt

<details>
<summary><b>Describe your Frontend (Prompt)**</b></summary>
```
Design a minimal and visually appealing podcast interface. The interface should feature:
A prominent text input field labeled "Type podcast topic here..." where users can enter their desired podcast topic.
A "Generate Podcast" button, incorporating a speaker emoji, that triggers the podcast generation process. The button should exhibit a color change on hover.
A loading animation (e.g., pulsing dots) displayed while the podcast is being generated.
An audio player area that initially displays "Podcast will appear here."
Functionality: Upon clicking "Generate Podcast," the loading animation should appear for 2 -3 seconds, followed by the message "Feature coming soon!" in the audio player area.
Visual Style: Utilize soft pastel colors (with appropriate contrast) and rounded corners throughout the design to create a cute and friendly appearance.
Adaptive Design: Ensure the interface is flexible and adapts seamlessly to different screen sizes.

```
</details>

<b>Test the Interface</b>

- Type some sample text
- Click the Generate Podcast button
- See the loading animation
</details>

<details>
<summary>**Connecting the Frontend to n8n Workflow**</summary>
<br>

<b>Providing Data to n8n</b>

- To generate a podcast, n8n needs information We'll send this data in a specific format.

`{"text": "whatever topic they typed"}`

<b>The Missing Link</b>
<br>
We need to create a bridge between:

- The beautiful interface (what people see) and n8n podcast generator workflow (what creates the podcast)

<b> Webhooks</b>

- A webhook serves as a bridge between the frontend application and n8n workflow by automatically receiving incoming data 

<b>WebHook Node</b>

- A webhook node act as a trigger node for a workflow when you want to receive data and run a workflow based on the data
- It is essentially a `URL endpoint` that listens for incoming data

<b>Webhooks - The Bridge Builder!</b>

- Think of a webhook like giving your workflow a phone number on the internet:

    - Your frontend knows this phone number
    - It "calls" this number with the user's text - whenever a user enters text and presses the button
    - Your workflow "answers" - processes the input and generates the podcast
    - It "calls back" with the finished audio file - returns the final result

<b>Replace Chat Trigger with Webhook</b>

<MultiLineWarning text="Why this change?">

- Chat Trigger only works inside n8n
- Webhook works from anywhere on the internet

</MultiLineWarning>
<b>**Steps to Update:</b>

1. Open your existing Podcast Generator workflow in n8n
2. Delete the Chat Trigger node
3. Add a Webhook node as the starting point
4. Configure the Webhook node settings

<b> Configuring the Webhook Node:</b>

- Open the Webhook node settings
1. Set `HTTP Method` to `POST`
3. Set `Response Mode` to `Respond to Webhook`
4. Copy the generated webhook URL (looks like: `https://your-n8n.app/webhook/abc123xyz`)

<b> How Webhooks Work </b>

- The frontend sends data to the webhook URL, and the webhook passes it to your workflow for processing

<b>Updating Data Connections</b>

- Connect Webhook to basic LLM chain node
- In LLM chain settings :
    - In the Source for Prompt (User Message), change dropdown to `Define below`
    - Update the input value to: `{{ $json.body.text }}`
- Similarly, update the System prompt placeholder to: 
    `{{ $json.body.text }}`
- This captures the text that comes from your frontend
- Keep all other connections the same

<b> Updating Data Connections</b>

- Complete Workflow Flow
    Webhook (Receives text) → LLM Chain (Processes text) → Gemini → Murf.ai

<b>Current Situation</b>

Right now, the workflow:

- Receives data from frontend
- Processes the request
- Generates podcast audio
- But the audio is stuck inside n8n!

The frontend is waiting for a response, but none has been sent yet.

<b> Send Data Back – Respond to Webhook Node</b>

- A node that completes the webhook conversation
- Takes data from your workflow
- Sends it back to whoever called the webhook

<b>Set up the Response Node</b>

- Add `Respond to Webhook` node after your HTTP Response/Podcast Downloader node
- In the node settings, configure:
    - `Respond With`: Binary File (because our output is audio)
    - `Response Data Source`: Automatically from Input
- This ensures the workflow sends the generated audio back as a downloadable file or playable URL to the frontend.


</details>

<details>
<summary>**Connecting Everything Together**</summary>
<br>

<b>Specifying Frontend Integration Details</b>

- Previously, we created a basic frontend without specifying:
    - Which webhook URL to call?
    - What data format to expect?
    - How to handle the response?

<b>Connecting the Frontend to n8n</b>

- Now we will update our frontend with the actual connection details from our n8n workflow configuration

<b>Update your Frontend</b>

- Go back to your Lovable project
- Copy your webhook URL from n8n
- Paste the connection prompt, replacing [PASTE YOUR WEBHOOK URL HERE] with your actual webhook URL
- Wait for Lovable to update the interface
- Preview the updated interface

<details>
<summary><b>Updated Prompt</b></summary>
```
Update the podcast interface to connect with this web address: [PASTE WEBHOOK URL HERE]

When someone clicks Generate Podcast:
Take the text they typed about their podcast topic
Send it to the web address in this format: {"text": "the topic they typed"}
Show loading dots saying "Creating podcast... please wait!"

When the response comes back:
It will contain {"audioFile": "link to the podcast"}
Show this audio in the player using the audioFile link
Display message " Podcast is ready! Click play to listen"

If something goes wrong:
Show "Oops! Something went wrong. Please try again"

After successful generation:
Clear the text box for next topic
Keep all the beautiful design from before
```
</details>

<b> What Happens Behind the Scenes </b>
<br>

The Complete Flow

#### 1. Frontend
- Packages the topic as JSON
- Sends data to n8n webhook

#### 2. n8n Webhook
- Receives the JSON data
- Triggers the workflow

#### 3. Audio File URL
- Workflow processes and generates audio
- Returns audio file URL

#### 4. Podcast Player
- Waits for the audio file URL
- Shows the podcast player when ready
- User can play the generated podcast

<b>Test the Complete System</b>
#### Step-by-Step Testing

- Execute the workflow in n8n (to keep it ready)  
2. Open your Lovable preview  
3. Type a podcast topic (e.g., "Generative AI")  
4. Click the `Generate Podcast` button  
5. Watch the loading animation appear  
6. Switch to the n8n tab — see nodes turning green as workflow executes  
7. Wait 10-30 seconds for processing  
8. Return to Lovable — audio player appears with your podcast  
9. Click `Play` and listen to your AI-generated podcast!

<b> Workflow Should be in Active State</b>
<br>
To ensure your workflow is automated and triggers as expected, make sure the workflow is active

- Open your workflow in n8n
- Toggle the workflow status to Active
- The workflow will now automatically respond to incoming webhook requests

<MultiLineNote>
- The Active button has been updated to Publish, allowing you to publish your workflows.
- Kindly note that the Publish feature is restricted to a limited number of uses on the portal.
</MultiLineNote>
</details>

<details>
<summary>**Deploy our Application**</summary>

- Right now, your app works in Lovable's preview
` Deployment gives it a real home on the internet where anyone can visit! `

<b>Deployment</b>

- In Lovable, click the Publish button (top right corner)
- Wait 1-2 minutes while Lovable deploys your project
- Receive your public URL (format: https://yourapp.lovable.app)
- Share the URL with friends and family!
</details>
---

###Before vs After

<b>BEFORE:</b>

- Workflow hidden inside n8n
- Only works with Chat Trigger
- Can't share with others
- Manual execution required

<b>AFTER:</b>

- Professional web application
- Beautiful public interface
- Anyone can use it
- Your own podcast generation service!