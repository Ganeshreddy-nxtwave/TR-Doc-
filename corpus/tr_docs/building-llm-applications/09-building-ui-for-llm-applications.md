# Building UI for LLM Applications

**Course:** Building LLM Applications  
**Topic:** Building UI and Deploying LLM Applications  
**Unit ID:** `a080f25ece564b6a9466c8ab50ca89e0` | **Unit Number:** 9

---

# Introduction

In previous sessions, we focused on building LLM applications using Python, specifically making our Study Assistant smarter by utilizing **System Prompts** and **Generation Settings**. Now, we'll shift our focus to **Building User Interfaces for LLM Applications**.

## The Problem with Just Code

Currently, our code can only be run within a coding environment. This presents a challenge:

- What if we want to make our application more presentable and usable by others?

## The Solution: UI and Deployment

To make our LLM applications truly accessible and user-friendly, we need two key components:

1.  **A Simple UI**: To allow people to easily interact with the app.
2.  **Deployment**: So anyone can access it online without needing to run it locally.

## Understanding UI for Web Applications

When we think about the applications we use every day, they all started as code written by developers but were transformed into real applications through a User Interface (UI).

Traditionally, building a web application requires:

- Using HTML/CSS for the interface
- Using JavaScript for interactivity
- Setting up and managing servers
- Understanding web development frameworks

However, for AI/ML projects, there are tools specifically designed to simplify this process. These tools allow you to focus on your Python code while automatically handling the interface and hosting.

### UI-Building Approaches

There are several ways to turn Python code into a usable interface:

1.  **UI building frameworks (e.g., Gradio, Streamlit)**
2.  **Full code options (HTML/CSS/JS frameworks)**
3.  **No-code/low-code builders**

In this session, we will be using **Gradio** due to its efficiency in rapidly creating web applications from Python code.

## Introduction to Gradio

Gradio is an open-source Python library that simplifies the process of turning your code into a shareable web application. It allows you to create interactive AI demos, such as chatbots or image generators, without the need to build a full website using traditional web development technologies.

### What Gradio Offers

-   **Different input types**: Text boxes, sliders, dropdowns, chat windows, and even image or webcam inputs.
-   **Multiple output types**: Text, images, audio, plots.
-   **Automatic web interface generation**: No HTML/CSS needed, as Gradio handles it for you.
-   **Built-in sharing**: Can create temporary public links instantly.

### Understanding the Gradio Workflow

Gradio's primary role is to:

1.  Create a visual interface for your input (e.g., text boxes, buttons).
2.  Take what the user types/selects from the UI.
3.  Pass this input to your Python function.
4.  Display the result from your Python function in a user-friendly format.

Gradio manages the web components, handles data flow between the UI and your Python function, and displays results in real-time.

## Building UI for Study Assistant with Gradio

Let's integrate Gradio into our Study Assistant application step by step.

### Initial Python Code (from previous session)

Our **Study Assistant**, which answers questions with a chosen personality:

```python
from google import genai
from google.colab import userdata
from google.genai import types

client = genai.Client(api_key=userdata.get('GEMINI_API_KEY'))

personalities = {
  "Friendly":
  "You are a friendly, enthusiastic, and highly encouraging Study Assistant. Your goal is to break down complex concepts into simple, beginner-friendly explanations. Use analogies and real-world examples that beginners can relate to. Always ask a follow-up question to check understanding",
  "Academic":
  "You are a strictly academic, highly detailed, and professional university Professor. Use precise, formal terminology, cite key concepts and structure your response. Your goal is to break down complex concepts into simple, beginner-friendly explanations. Use analogies and real-world examples that beginners can relate to. Always ask a follow-up question to check understanding"
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

question = "What are LLMs?"
personality = "Friendly"
print(study_assistant(question, personality))
```

### Installing Gradio

First, install the Gradio library in your environment:

```python
!pip install -q gradio
```
-   `!pip install -q gradio`: This command installs the Gradio Python library. The `!` tells the environment (like Colab) to execute a shell command, `pip` is the Python package installer, and `-q` means "quiet" installation, suppressing verbose output.

### Importing Gradio
```python
import gradio as gr
```
-   `import gradio as gr`: This imports the Gradio library and assigns it the alias `gr` for easier use in code.

### Creating the Gradio Interface

Gradio provides a special class called `Interface` to quickly create a demo for your Python function.

#### Syntax for `Interface()`

The `gr.Interface()` class takes several key parameters:

-   `fn`: The Python function that Gradio should run when the user interacts with the UI.
-   `inputs`: Defines how to take input for your function (e.g., `gr.Textbox`, `gr.Radio`).
-   `outputs`: Defines how to display the output from your function.
-   `title`: The title of your application, displayed at the top of the UI.
-   `description`: A short description shown below the title.

#### Input and Output Types in Gradio

Gradio offers a variety of components for inputs and outputs:

-   **Inputs**: `gr.Textbox`, `gr.Radio`, `gr.Dropdown`, `gr.Image`, `gr.Slider`, etc.
-   **Outputs**: `gr.Textbox`, `gr.Image`, `gr.JSON`, `gr.Audio`, `gr.Plot`, etc.

#### Full Gradio UI Code for Study Assistant

Now, let's put it all together to create the Gradio interface for our `study_assistant` function:

```python
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

```
### Launching the App

To make your Gradio application run and be accessible:

```python
demo.launch(debug=True)
```
-   `demo.launch(debug=True)`: This command starts the Gradio web server. 
- `debug=True` provides additional debugging information in the console, which is useful during development.

### Final Code

```python
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