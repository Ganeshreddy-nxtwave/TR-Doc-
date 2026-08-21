# Effective Prompting Techniques

**Course:** Building LLM Applications  
**Topic:** Tools Use & Function Calling in LLMs  
**Unit ID:** `eeca3724eecd493dbbb5ae525b58741c` | **Unit Number:** 21

---

# Effective Prompting Techniques

## Introduction

Effective prompting is crucial for getting the best results from Large Language Models (LLMs). When instructions are given in plain paragraphs, AI may miss details, skip steps, or format answers inconsistently. This guide covers several advanced techniques to help you create clear, structured, and powerful prompts.

---

## 1. Structured Prompting

Structured prompting is a method of writing prompts in formal formats like JSON or TOON to guide the AI in producing clear, organized, and consistent responses. Instead of guessing your intent, the model is told exactly what you want.

### Problem with Unstructured Prompts

When instructions are given in plain paragraphs, an AI might:

- Miss important details
- Skip steps in a multi-step task
- Format the output inconsistently

This can lead to incorrect, messy, or unpredictable results.

### Structured Prompting with JSON

Using JSON format in your prompts helps in defining the task and the desired output structure clearly.

**Example 1: Normal vs. JSON Prompt**

*   **Normal Prompt:**

    ```
    Provide summary about Generative AI in 300 words
    ```
*   **JSON Prompt:**

    ```json
    {
      "task": "summarize_topic",
      "topic": "Generative AI",
      "style": "informative and clear",
      "length": "approximately 300 words"
    }
    ```
The JSON version is more explicit, leading to a crisper and more relevant response.

**Example 2: Data Extraction**

```json
{
  "task": "extract_order_details",
  "output_format": {
    "customer_name": ",
    "phone": ",
    "product": ",
    "quantity": ",
    "delivery_location": "
  },
  "text": "Hi, I want to order 2 iPhones for delivery to Bangalore. My name is Riya, phone number 9876543210."
}
```

### When to Use Structured Prompting

1.  **Data extraction** for automation.
2.  When you want **accurate and clear responses**.
3.  When sending AI output to a **backend API or database**.
- When working with **Multi-step agent workflows**

### Benefits of Structured Prompting

- Makes AI answers organized and predictable.
- Minimizes errors and misinterpretations.
- Saves time in parsing and debugging the output.

### The TOON Format: A More Efficient Alternative

A problem with JSON is its verbosity. It uses a lot of punctuation (`{}`, `[]`, `"`, `:`, `,`) and repeats keys, which consumes more tokens and increases costs.

**Token-Oriented Object Notation (TOON)** is a lightweight format that uses minimal punctuation, reducing token count and cost.

**JSON vs. TOON Comparison**

 **Example:**
JSON prompt:

 ```json
 {
  "task": "extract_order_details",
  "output_format": {
    "customer_name": ",
    "phone": ",
    "product": ",
    "quantity": ",
    "delivery_location": "
  },
  "text": "Hi, I want to order 2 iPhones for delivery to Bangalore. My name is Riya, phone number 1234567890."
} 
``` 
Tokens used in JSON Prompt: ~105-110

TOON Prompt:

```Toon
task: extract_order_details
fields[5]{customer_name,phone,product,quantity,delivery_location}:
Hi, I want to order 2 iPhones for delivery to Bangalore. My name is Riya, phone number 1234567890.

```
Tokens used in TOON Prompt: ~70-75

### Why TOON Produces Better Results

- **Schema Declared Once**: TOON lists all field names once.
- **Minimal Punctuation**: It uses CSV-style rows.
- **Explicit Array Length**: TOON shows (used [5] in the above example) to indicate the number of fields.

---

## 2. Meta Prompting

Meta-prompting involves using the language model itself to generate or improve prompts before you use them for the final task.

### Why Use Meta Prompting?

- Gets better, clearer, and more creative answers.
- Saves time by reducing trial-and-error with prompts.
- Helps with complex or multi-step problems

### Example 1


    You are an expert prompt engineer. Your task is to create an effective prompt for {generating product descriptions}. Consider including guidelines for tone, structure, and key elements to include. The prompt should instruct the AI to: {write compelling, accurate, and concise descriptions for 
    various products on an e-commerce website} 

    
    
### Example 2

Instead of a basic prompt, you use a meta-prompt to first generate a better prompt.

*   **Basic Prompt:**

    ```
    “Write an SEO-optimized blog about why LLMs are important
    ```
    
*   **Meta-prompt:**

    ```
    You are a wizard prompt engineer. You write very bespoke, detailed, and succinct prompts. I want you to write me a prompt that will {{ write a blog about importance of LLM with SEO optimization }}
    ```

The model will first generate a highly detailed prompt, which you can then use to get a superior final output.

---

## 3. Prompt Chaining

Prompt chaining is a technique where a task is broken down into a series of smaller prompts. The output from one prompt is used as the input for the next, guiding the model to produce a more coherent and accurate final result.


### Implementation Steps

1. Split the task into smaller, logical subtasks.
2. Write clear prompts for each step.
3. Pass the output of one step sequentially as input to the next.

### Example: Creating a Revision Sheet

**Task**: Create a summary of a topic, generate questions from it, and combine both into a final revision sheet.
**Example:**

- Initial Code:

```python
from google import genai
from google.colab import userdata

client = genai.Client(api_key=userdata.get("GEMINI_API_KEY"))

# Revision buddy Function
def revision_buddy(user_prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt
    )
    return response.text
response = revision_buddy("Explain about Generative AI")
print("Output:\n", response)

```

1. Chain Step 1: Summarize the topic

```python
summary = revision_buddy("Summarize Operating System basics in bullet points.")
print("SUMMARY:\n", summary)
```

2. Chain Step 2: Create Questions

Second step uses the result from the first step - this is Prompt Chaining

```python
questions = revision_buddy(f"Generate 5 exam questions from this summary:\n{summary}")
print("\nQUESTIONS:\n", questions)
```

3. Chain Step 3: Create Final Revision Sheet

Subsequent step uses the result from previous steps — this is Prompt Chaining

```python
revision_sheet = revision_buddy(
    f"Create a final revision sheet using this summary and questions.\n"
    f"Summary:\n{summary}\nQuestions:\n{questions}"
)
print("\nREVISION SHEET:\n", revision_sheet)
```
---

## 4. Prompt Base

PromptBase is a marketplace website where people can buy and sell high-quality prompts for AI tools like ChatGPT, DALL-E, and Midjourney.

<MultiLineNote>
Free prompts are also available in PromptBase
</MultiLineNote>

### Getting Started on PromptBase

1.  **Make an account** in <a href="https://promptbase.com/" target="_blank">PromptBase</a> and set up your profile.
2.  **Upload prompts** that are clear, creative, and have been tested.
3.  **Use relevant keywords** so people can find your prompts easily.

---

## 5. General Effective Prompting Tips

### Clarity
Use simple and clear wording so the AI understands exactly what you want.

*   **Generic Prompt:** “Describe a cell”
*   **Precise Prompt:** “Describe the parts of a human cell in 3 sentences: nucleus, cytoplasm, and membrane”

### Specificity
Add details like length, tone, or format to get a more precise answer.

*   **Generic Prompt:** “Write a story”
*   **Precise Prompt:** “Write a 500-word detective story set in London in the 1920s about a missing painting”

### Contextual Awareness
Give background information, such as who the answer is for (audience), what role the AI should play, or the situation.

*   **Generic Prompt:** “What are the causes of the French Revolution?”
*   **Precise Prompt:** “You are a high school teacher. Explain 3 causes of the French Revolution in simple words for students”

### Output Guidance
Tell the AI the exact format or structure you expect in the output.

*   **Generic Prompt:** “Compare iPhone and Android”
*   **Precise Prompt:** “Make a comparison table with columns for price, features, and ecosystem, then add a 2-sentence conclusion”

### Adaptability
Use reusable prompt templates for consistent results across similar tasks.

*   **Template:** 

```
Summarize [topic] in 3 bullet points for [audience]. Add one real-world example.
```