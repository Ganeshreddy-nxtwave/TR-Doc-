# Building LLM Applications Using Python Part 2

**Course:** Building LLM Applications  
**Topic:** Building LLM Applications Using Python  
**Unit ID:** `7e2c259c689c41d488e5c0b0c2dcc486` | **Unit Number:** 7

---

# Building LLM Applications using Python | Part 2

## Introduction

In previous session, we built a basic study assistant that could answer questions using a Large Language Model (LLM). It was functional but behaved like a generic chatbot.

---

## Making the Study Assistant Smarter

Right now, our assistant just passes a question to the LLM. It works, but it behaves like a generic chatbot, Let's set overall behavior, guidelines, and context for the AI so that it will break down the concepts and explain in clear and understandable way


### To make our Study Assistant smart:

1.  **Add Personality**: Make the assistant respond in a specific style (e.g., Friendly, Academic).
2.  **Set Overall Behaviour**: Define clear instructions for how the assistant should act.
3.  **Control the Output**: Manage the length and creativity of the generated text.

The overall flow for our enhanced assistant will be:

**Input** → **Prompt Construction** → **Model Call** → **Output**

---

## Understanding Chat Model Roles

When you interact with a conversational LLM, the conversation is structured using three distinct roles: **System**, **User**, and **Assistant**. Understanding this structure is key to guiding the AI's behavior.

-   **System**: These are the background instructions you give the AI before the conversation starts. It sets the overall behavior, tone, personality, and rules. Think of it as telling the AI, "Hey, behave like a professional coach" or "Explain this concept to a complete beginner."

-   **User**: This is your actual input, the question or task you provide to the AI.

-   **Assistant**: This is the AI's response based on your instructions and the preceding conversation. The history of assistant responses provides context for follow-up interactions.

The **System Prompt** is the most powerful tool for guiding the AI’s behavior before you even ask your question.

---

## Implementing System Prompts

A **System Prompt** is a short instruction that tells the LLM how to behave before it answers anything. It sets the tone, personality, and rules for the assistant.

<details>
<summary><strong>Python code for updating prompt of the Study Assistant</strong></summary>

```python
from google import genai
from google.colab import userdata

client = genai.Client(api_key=userdata.get("GEMINI_API_KEY"))

def study_assistant(question):
  prompt = f"You are my smart Study Assistant. Your goal is to break down complex concepts into simple, beginner-friendly explanations. Use analogies and real-world examples that beginners can relate to. Always ask a follow-up question to check understanding. Here is my question: {question}"
  response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
  )
  return response.text
```

</details>

---

## Adding Personalities through System Prompts

We can make our assistant more dynamic by defining multiple personalities and letting the user choose one. A Python dictionary is a great way to store these predefined personalities. The `GenerateContentConfig` object is the mechanism through which we pass the selected system instruction (personality) to the Gemini model.

<details>
<summary><strong>Python code for defining and using personalities</strong></summary>

We'll create a dictionary where each key is a personality name and the value is the corresponding system prompt.

```python
personalities = {
  "Friendly": "You are a friendly, enthusiastic, and highly encouraging Study Assistant. Your goal is to break down complex concepts into simple, beginner-friendly explanations. Use analogies and real-world examples that beginners can relate to. Always ask a follow-up question to check understanding.",
  "Academic": "You are a strictly academic, highly detailed, and professional university Professor. Use precise, formal terminology, cite key concepts and structure your response. Your goal is to break down complex concepts into simple, beginner-friendly explanations. Use analogies and real-world examples that beginners can relate to. Always ask a follow-up question to check understanding."
}
```

Next, we update our `study_assistant` function to accept a `persona` argument. This argument will be used as a key to retrieve the correct system prompt from our `personalities` dictionary.

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
        ),
        contents=question
    )
    return response.text

question = "What are LLMs?"
personality = "Friendly"
print(study_assistant(question, personality))
```

</details>

---

## Controlling Generation Settings

Beyond personality, we can also control *how* the model generates its responses. The two most important settings for this are **temperature** and **maximum output tokens**.

### Temperature

**Temperature** controls the randomness of the model's output. Increasing the temperature value increases the randomness of the output. For Gemini, the range is typically from 0 to 2.

-   **Temperature = 0 (Deterministic)**: The model becomes very focused and consistent. The same input will almost always produce the same output. Best for factual answers, code generation, or math.
-   **Temperature = 0.7 (Balanced)**: A good mix of consistency and creativity. It produces some variation in responses, making it ideal for most general applications.
-   **Temperature = 1.2+ (Creative)**: The model becomes very random and creative, leading to unexpected and varied responses. Best for creative writing, brainstorming, or storytelling.

### Max Tokens

**Tokens** are the chunks of text the model processes (e.g., words, parts of words). We can set `max_output_tokens` to control the length of the response.

Just as there's a limit to the output length, there's also a maximum limit to the length of the input prompt, sometimes referred to as `max_input_tokens`. This limit is crucial to avoid errors and varies depending on the specific model used.

Why control tokens?

- **Control costs**: You pay per token (both input and output).
- **Keep responses concise**: Prevent overly long answers.

**Typical Ranges:**

-   **50-100 tokens**: A short answer (one paragraph).
-   **500-1000 tokens**: A medium response (a few paragraphs).
-   **2000+ tokens**: A long response (essay-length).

<details>
<summary><strong>Final python code</strong></summary>

We can add `temperature` and `max_output_tokens` to the same `GenerateContentConfig` object where we defined our system prompt.

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
            max_output_tokens=1000
        ),
        contents=question
    )
    return response.text

question = "What are LLMs?"
personality = "Friendly"
print(study_assistant(question, personality))
```
</details>

---

## Rate Limits and Costs

When working with APIs, there are practical limitations to keep in mind:

-   **Rate Limits**: This defines how many requests per minute your app can send (e.g., 60 requests/minute). Exceeding this limit will result in a `RateLimitExceededError`.
-   **Token Allowances**: Free tiers often have caps on the number of tokens you can use per day or per month. Remember that "tokens" includes both your input prompt and the model's output. Large inputs will consume your allowance faster.

---

## ServerError
Occasionally, you might encounter a `ServerError` when interacting with the Gemini API. This typically indicates an issue on the server-side, such as the Gemini service being temporarily unavailable, undergoing maintenance, or experiencing high traffic. In such cases, retry executing your code after sometime.