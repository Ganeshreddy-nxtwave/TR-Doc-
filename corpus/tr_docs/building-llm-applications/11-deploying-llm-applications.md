# Deploying LLM Applications

**Course:** Building LLM Applications  
**Topic:** Building UI and Deploying LLM Applications  
**Unit ID:** `692eb3b5bd884c51bc8539c8933191ed` | **Unit Number:** 11

---

# Introduction

In the previous sessions, we've built powerful LLM applications that run in our local environments like Google Colab. Now, it's time to take the final step: deploying our application to make it accessible to anyone in the world.

This unit will guide you through the process of deploying an LLM application using Hugging Face Spaces, transforming your code into a fully functional web app.

# Understanding Deployment

Right now, our Study Assistant application exists only within our Google Colab. This means only we can run it, and it's only active while our Colab notebook is running.

**Deployment is the process of moving our application from our local environment to a publicly accessible server on the internet.**

We will use **Hugging Face Spaces** to serve our application.

## What are Hugging Face Spaces?

Hugging Face Spaces is a free hosting service provided by Hugging Face, specifically designed for showcasing AI and machine learning applications.

### How It Works

The process is straightforward:

1.  **Upload Files**: We upload our application code (`app.py`) and a list of dependencies (`requirements.txt`).
2.  **Add Secret Keys**: We securely add our API keys (like the Gemini API key) without exposing them in our code.
3.  **Automatic Deployment**: Hugging Face automatically builds and deploys our application on the cloud.
4.  **Get a Live URL**: We receive a permanent, public URL that we can share with anyone. The app stays online 24/7 (with some limitations).

---

# Preparing for Permanent Deployment

When we use `demo.launch()` in Gradio, it creates a temporary, shareable link that only works while our Colab notebook is active. For permanent deployment, we need to package our code into files that can run independently on a server.

We'll need two main files:
1.  `app.py`: Contains our application's Python code.
2.  `requirements.txt`: Lists all the Python libraries our app needs to run.

### Code Modifications for Deployment

Before we can deploy, we need to make two simple but crucial modifications to our Study Assistant code.

<details>
<summary><strong>First Modification: Create `app.py` File</strong></summary>

To package our code into a file, we can use a "magic command" in our Colab notebook. By adding `%%writefile app.py` at the very top of the cell containing our application code, we instruct Colab to save the entire cell's content into a file named `app.py`.

```python
%%writefile app.py
import gradio as gr
from google import genai
from google.genai import types
from google.colab import userdata

client = genai.Client(api_key=userdata.get("GEMINI_API_KEY"))

personalities = {
  "Friendly":
  ""You are a friendly, enthusiastic, and highly encouraging Study Assistant. 
  Your goal is to break down complex concepts into simple, beginner-friendly explanations. 
  Use analogies and real-world examples that beginners can relate to. 
  Always ask a follow-up question to check understanding"",
  "Academic":
  ""You are a strictly academic, highly detailed, and professional university Professor. 
  Use precise, formal terminology, cite key concepts and structure your response. 
  Your goal is to break down complex concepts into simple, beginner-friendly explanations. 
  Use analogies and real-world examples that beginners can relate to. 
  Always ask a follow-up question to check understanding""
}

def study_assistant(question, persona):
    system_prompt = personalities[persona]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.4,
            max_output_tokens=2000
        ),
        contents=question
    )
    return response.text

demo = gr.Interface(
    fn=study_assistant,
    inputs=[
        gr.Textbox(lines=4, placeholder="Ask a question...", label="Question"),
        gr.Radio(choices=list(personalities.keys()), value="Friendly", label="Personality")
    ],
    outputs=gr.Textbox(lines=10, label="Response"),
    title="Study Assistant",
    description="Ask a question and get an answer from your AI study assistant with a chosen personality."
)

demo.launch(debug=True)
```
</details>

<details>
<summary><strong>Second Modification: Access API Key from Environment Variables</strong></summary>

Our current code gets the API key from Colab's secrets manager, which won't be available in Hugging Face. We need to modify it to read the key from the server's "environment variables" (which Hugging Face calls "Secrets").

1.  **Remove Colab-specific import**: We no longer need to import `userdata` from `google.colab`.
2.  **Add `os` import**: We'll use Python's built-in `os` library to access environment variables.
3.  **Update genai.Client**: We'll change how the client is initialized to use `os.getenv()`.

**From this:**

```python
from google.colab import userdata
client = genai.Client(api_key=userdata.get("GEMINI_API_KEY"))
```

**To this:**

```python
import os
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
```
This tells our app to look for a secret named `GEMINI_API_KEY` in the Hugging Face environment.

#### **Final `app.py` Code Structure**
```python
%%writefile app.py
import gradio as gr
from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

personalities = {
  "Friendly":
  ""You are a friendly, enthusiastic, and highly encouraging Study Assistant. 
  Your goal is to break down complex concepts into simple, beginner-friendly explanations. 
  Use analogies and real-world examples that beginners can relate to. 
  Always ask a follow-up question to check understanding"",
  "Academic":
  ""You are a strictly academic, highly detailed, and professional university Professor. 
  Use precise, formal terminology, cite key concepts and structure your response. 
  Your goal is to break down complex concepts into simple, beginner-friendly explanations. 
  Use analogies and real-world examples that beginners can relate to. 
  Always ask a follow-up question to check understanding""
}

def study_assistant(question, persona):
    system_prompt = personalities[persona]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.4,
            max_output_tokens=2000
        ),
        contents=question
    )
    return response.text

demo = gr.Interface(
    fn=study_assistant,
    inputs=[
        gr.Textbox(lines=4, placeholder="Ask a question...", label="Question"),
        gr.Radio(choices=list(personalities.keys()), value="Friendly", label="Personality")
    ],
    outputs=gr.Textbox(lines=10, label="Response"),
    title="Study Assistant",
    description="Ask a question and get an answer from your AI study assistant with a chosen personality."
)

demo.launch(debug=True)
```
</details>

<details>
<summary><strong>Creating the `requirements.txt` File</strong></summary>

Next, we need to tell Hugging Face which Python libraries to install. We do this by creating a `requirements.txt` file.

In a new cell in your Colab notebook, use the `%%writefile` command again:

```python
%%writefile requirements.txt
gradio
google-genai
```
This file lists the `gradio` and `google-genai` packages, which Hugging Face will automatically install before running our app.

<MultiLineWarning text="Important">
After running both `%%writefile` cells, you must download the newly created `app.py` and `requirements.txt` files from the Colab file browser. You will need them for the next steps.
</MultiLineWarning>

</details>

---

# Step-by-Step Deployment Process

Now that we have our files ready, let's deploy our app to Hugging Face Spaces.

<details>
<summary><strong>Step 1: Create a Hugging Face Account</strong></summary>

-   Go to <a href="https://huggingface.co" target="_blank">huggingface.co</a>
-   Click **"Sign Up"** in the top right.
-   Create a free account. You can sign up with Google or GitHub for a faster process.
</details>

<details>
<summary><strong>Step 2: Create a New Space</strong></summary>

-   Once logged in, click your profile icon (top right) and select **"New Space"**.
-   Configure your Space with the following settings:
    -   **Space name**: Choose a unique name for your app (e.g., `my-study-assistant`).
    -   **License**: `MIT`
    -   **Space SDK**: `Gradio`
    -   **Template**: `Blank`
    -   **Hardware**: `CPU basic` (this is free and sufficient).
    -   **Visibility**: `Public`
-   Click **"Create Space"**.
</details>

<details>
<summary><strong>Step 3: Add Your API Key as a Secret</strong></summary>

This is a critical step for security. We must never paste our API key directly into our code.

-   In your new Space, click the **"Settings"** tab.
-   Scroll down to the **"Variables and secrets"** section.
-   Click **"New secret"**.
-   Fill in the details:
    -   **Name**: `GEMINI_API_KEY` (This must match exactly what's in `os.getenv("GEMINI_API_KEY")`).
    -   **Secret value**: Paste your actual Gemini API key here.
-   Click **"Save secret"**.

Now your app can securely access the key without exposing it to the public.
</details>

<details>
<summary><strong>Step 4: Upload Your Files</strong></summary>

-   Go to the **"Files"** tab in your Space.
-   Click the **"Contribute"** button and select **"Upload files"**.
-   Drag and drop (or select) both your `app.py` and `requirements.txt` files.
-   Add a commit message (e.g., "Initial commit").
-   Click **"Commit changes to main"**.
</details>

<details>
<summary><strong>Step 5: Wait for the Build and Test Your App!</strong></summary>

Once you commit the files, Hugging Face automatically starts the build process. You will see a "Building" status. This might take 1-2 minutes.

-   Hugging Face creates a Python environment.
-   It installs the packages from `requirements.txt`.
-   It runs your `app.py` file.

Once complete, your Gradio application will appear directly on the page! You can now interact with it live.

### Share Your Link

Your app is now live at a permanent URL. You can find it in your browser's address bar. The format will be:
`https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`

You can share this link with friends, add it to your portfolio, or include it in your resume!
</details>

---

# Understanding Free Space Limitations

Hugging Face's free tier is fantastic for student projects and demos, but it has some limitations:

<details>
<summary><strong>Sleep Mode</strong></summary>
If your app is inactive for about 48 hours, it will "sleep" to conserve resources. The first person to visit it after it sleeps will experience a short loading time (around 20 seconds) as the app wakes up.
</details>

<details>
<summary><strong>Performance</strong></summary>
The free tier has limited CPU and RAM. If your app gets a lot of traffic at once, it may slow down.
</details>

<details>
<summary><strong>Storage</strong></summary>
There is limited storage space, so it's not suitable for applications that need to store very large files.
</details>