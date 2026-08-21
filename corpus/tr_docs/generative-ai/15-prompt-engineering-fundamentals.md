# Prompt Engineering Fundamentals

**Course:** Generative AI  
**Topic:** Productivity Power-Up with AI Tools & Prompt Engineering Fundamentals  
**Unit ID:** `54f96653b41041d9843a9b8a86517f53` | **Unit Number:** 15

---

# Introduction 

In the previous unit, we explored how AI tools can enhance productivity, from creating presentations to understanding complex code and automating tasks.
In this unit, we dive into prompt engineering, the art of crafting clear and detailed prompts to help large language models (LLMs) generate accurate and high-quality answers. We’ll cover the fundamentals, techniques, and best practices for effective prompt creation.


#Prompt Engineering Fundamentals

Have you ever asked an LLM a question and received a confusing or unhelpful response?

<MultiLineNote>Better Prompt… Better Results..!</MultiLineNote>


The natural language text, which describes the task that an LLM should perform, is called a prompt

##Examples

<details>
<summary><strong>Basic Prompt:</strong></summary>

```
What is generative AI?
```
</details>

<details>
<summary><strong>Better Prompt:</strong></summary>

```
I'm a first-year B.Tech student. Can you explain what generative AI is in simple terms, with examples of how it's used in apps like ChatGPT?
```

</details>

---

<details>
<summary><strong>Basic Prompt:</strong></summary>

```
How to prepare for exams?
```

</details>

<details>
<summary><strong>Better Prompt:</strong></summary>

```
I'm a first-year B.Tech student with exams in two weeks. Can you recommend a study plan that includes revision strategies, breaks, and how to handle difficult subjects?
```

</details>
<MultiLineQuickTip>If you observe carefully, the LLM response depends on how the question is asked. The clearer and more detailed your prompt is, the better the model output will be.</MultiLineQuickTip>
**Better Prompts Lead To Better Results!**

The clearer and more detailed your prompt is, the better the model output will be

#1. Prompt Engineering
Prompt engineering is the art of creating prompts that help an LLM generate more accurate and higher-quality answers

**Think of it like this**

- If an LLM is like a highly knowledgeable intern on their first day
- Prompt engineering is the skill of giving that intern clear, detailed instructions 

##Why Prompt Engineering?

- **Better results**: More accurate, relevant, and useful responses.
- **Consistency**: Well-engineered prompts produce reliable results each time.
- **Saves time**: Get what you need in fewer iterations.
- **Avoid confusion**: A clear prompt prevents the model from making incorrect assumptions.

## Be Clear and Direct

- Think of an LLM like a new intern
- It doesn't know what to do unless you explain it.
- It needs detailed instructions to perform correctly.

The more clearly and specifically you explain what you want, the better and more accurate the response will be.

<details>
<summary><strong>Basic Prompt:</strong></summary>

```
Write a resume
```
</details>

<details>
<summary><strong>Better Prompt:</strong></summary>

```
Can you help me create a professional resume for a BTech CSE student? Include sections like personal details, education, skills, internships, projects, and achievements. Please provide tips for each section to make the resume stand out to potential employers.
```
</details>

#3. Basic Prompt Structure

## The RCATF Framework

* **Role**: Defines the persona of the AI.  
* **Context**: Provides the background and limitations.  
* **Action/Task**: Specifies the task or question.  
* **Format**: Specifies the format of the output.  
* **Tone**: Defines the style or voice the AI should use.

## Role

- It is sometimes important to prompt the LLM to take on a specific role.  
- This technique is known as **role prompting**.  
- The more detail you provide about the role and context, the better the results.  
- Priming an LLM with a specific role can enhance its performance across various tasks, from writing to coding to summarizing.  
- It's like how humans can sometimes be helped when told to "think like a ______".  
- Role prompting can also change the style, tone, and manner of the LLM’s response.

<details>
<summary><strong>Examples</strong></summary>
- You are a professional chef with 20 years of experience in Italian cuisine.
- Act like a stand-up comedian from New York.
- You are a senior software engineer specializing in frontend development.

</details>
<details>
<summary><strong>Prompt</strong></summary>

```
Act as an experienced travel consultant who specializes in budget-friendly trips and has personally visited over 50 destinations."
```
</details>

## Context

- Context tells the LLM who it's helping, what the situation is, and any limitations.  
- Good context helps the LLM understand your specific needs.

<details>
<summary><strong>Examples</strong></summary>


- **Personal situation**: "I'm planning a trip to Japan."
- **Audience information**: "This is for high school students."
- **Project details**: "We're launching a new product next month."
- **Constraints**: "We have a limited budget."
- **Prior knowledge**: "I have no experience with coding."
</details>

<details>
<summary><strong>Prompt</strong></summary>

```
Role: Act as an experienced travel consultant who specializes in budget-friendly trips and has personally visited over 50 destinations."

Context: I'm a 22-year-old college student planning my first solo trip. I have a budget of 20,000, 10 days to travel in June, and I'm interested in both outdoor activities and experiencing local culture. I'm somewhat adventurous but also concerned about safety as a solo traveler.
```

</details>

## Action/Task

- The specific action or task you want the LLM to perform.  
- This is the "verb" of your prompt – the specific action you want the LLM to take.

<details>
<summary><strong>Examples</strong></summary>

- **Explain/teach**: "Explain Generative AI."
- **Create/generate**: "Create a marketing plan."
- **Analyze/evaluate**: "Analyze this paragraph."
- **Summarize**: "Summarize this research paper."
- **Compare/contrast**: "Compare these two approaches."
- **Brainstorm**: "Brainstorm names for my startup."
</details>

<details>
<summary><strong>Prompt</strong></summary>

```
Role: Act as an experienced travel consultant who specializes in budget-friendly trips and has personally visited over 50 destinations."

Context: I'm a 22-year-old college student planning my first solo trip. I have a budget of 20,000, 10 days to travel in June, and I'm interested in both outdoor activities and experiencing local culture. I'm somewhat adventurous but also concerned about safety as a solo traveler.

Action: Recommend 2 specific destinations that would be ideal for my situation, and for each destination, suggest a 10-day itinerary that balances cultural experiences, outdoor activities, and relaxation.
```

</details>

##Format
- Format tells the LLM how you want your answer organized and presented.

<details>
<summary><strong>Examples</strong></summary>

- Bullet points or numbered lists
- Table or chart
- Step-by-step guide
- FAQ style (question and answer)
- Timeline
- Markdown formatting with headers and subheaders
</details>

<details>
<summary><strong>Prompt</strong></summary>
```
Role: Act as an experienced travel consultant who specializes in budget-friendly trips and has personally visited over 50 destinations."

Context: I'm a 22-year-old college student planning my first solo trip. I have a budget of 20,000, 10 days to travel in June, and I'm interested in both outdoor activities and experiencing local culture. I'm somewhat adventurous but also concerned about safety as a solo traveler.

Action: Recommend 2 specific destinations that would be ideal for my situation, and for each destination, suggest a 10-day itinerary that balances cultural experiences, outdoor activities, and relaxation.

Format: For each destination, create a section that includes:
A short overview (3–5 sentences)
An estimated cost breakdown (accommodation, food, activities, transport)
Safety tips for solo travelers


Then provide a day-by-day itinerary in table format with columns for:
Day #
Morning activity
Afternoon activity
Evening activity
Accommodation
Finally, end with a pros and cons list for each destination
```
</details>

## Tone

The style, voice, or emotional quality you want the LLM to use in its response. This affects how the message feels to the reader.

<details>
<summary><strong>Examples</strong></summary>

- Formal or academic
- Friendly and conversational
- Encouraging and supportive
- Direct and concise
- Enthusiastic and energetic
- Cautious and balanced
- Simple and easy to understand

</details>
<details>
<summary><strong>Prompt</strong></summary>
```
Role: Act as an experienced travel consultant who specializes in budget-friendly trips and has personally visited over 50 destinations."

Context: I'm a 22-year-old college student planning my first solo trip. I have a budget of 20,000, 10 days to travel in June, and I'm interested in both outdoor activities and experiencing local culture. I'm somewhat adventurous but also concerned about safety as a solo traveler.

Action: Recommend 2 specific destinations that would be ideal for my situation, and for each destination, suggest a 10-day itinerary that balances cultural experiences, outdoor activities, and relaxation.

Format: For each destination, create a section that includes:
A short overview (3–5 sentences)
An estimated cost breakdown (accommodation, food, activities, transport)
Safety tips for solo travelers


Then provide a day-by-day itinerary in table format with columns for:
Day #
Morning activity
Afternoon activity
Evening activity
Accommodation
Finally, end with a pros and cons list for each destination

Tone: Include some humor where appropriate, and write as if you're a slightly older friend who wants to make sure I have an amazing but safe experience. Use casual language but don't skimp on important details.
```
</details>


#Example Prompt Templates
<details>
<summary><strong>Interview Preparation</strong></summary>

```
Template: "You're an experienced career counselor. I have an upcoming {{INTERVIEW_TYPE}} interview for a {{JOB_ROLE}} position. Provide me with 8-10 targeted practice questions I should prepare for, along with strategic tips for answering them effectively. Present this as a clear study guide with practical examples I can practice."
Inputs:
{{INTERVIEW_TYPE}}: "technical" / "behavioral" / "panel" / "phone screening" / "final round"
{{JOB_ROLE}}: "software engineer" / "marketing manager" / "data analyst" / "sales representative" / "project manager”

```
</details>


<details>
<summary><strong>Summarizing an Article</strong></summary>

```
Template: "You're a research assistant skilled at distilling complex information. I need to quickly understand the key insights from {{ARTICLE_TOPIC}}. Read through the content and create a concise summary that captures the main arguments, supporting evidence, and conclusions. Format this as bullet points with the most important takeaways first, using clear and objective language."
Inputs:
{{ARTICLE_TOPIC}}: "climate change research paper" / "new technology trends report" / "healthcare policy analysis" / "market research study" / "historical analysis piece"

```
</details>

#Tricks and Tips
##Separating Data from Instructions

- Instead of writing a new prompt each time, 
you can create a reusable prompt template and 
that can be reused with different data each time
- This is especially useful when you need 
the LLM to perform the same task repeatedly but with different input data

<details>
<summary><strong>Simple Template</strong></summary>

```
I will tell you the name of an animal. Please respond with the sound that animal makes. {{ANIMAL}}

```
</details>

## Why Separate Data from Instructions?

- **Reusability**: Create once, use multiple times with different data.
- **Consistency**: Same task structure ensures consistent results.
- **Clarity**: Keeps instructions separate from variable content.

<details>
<summary><strong>Example</strong></summary>

```
Template: "Explain {{CONCEPT}} at a {{LEVEL}} level with examples."
Inputs:
{{CONCEPT}}: "recursion in programming" / "object-oriented programming" / "Ohm’s Law" 
{{LEVEL}}: "high school" / "first year btech student" / "intermediate" / "advanced"

```

```
Final Prompt: "Explain recursion in programming at a high school level with examples."
```
</details>

##Additional Exploration

- **OpenAI Examples**:  
  [OpenAI Documentation Examples](https://platform.openai.com/docs/examples)  
  [OpenAI Cookbook](https://cookbook.openai.com/)

- **For Cross-Platform Exploration**:  
  [Google Cloud Vertex AI Prompt Gallery](https://cloud.google.com/vertex-ai/generative-ai/docs/prompt-gallery)

- **Additional Prompt Resources**:  
  [Microsoft Prompts for Education - Students](https://github.com/microsoft/prompts-for-edu/tree/main/Students/Prompts)  
  [OpenAI Examples](https://platform.openai.com/docs/examples)  
  [Google Cloud Vertex AI Prompt Gallery](https://cloud.google.com/vertex-ai/generative-ai/docs/prompt-gallery)  
  [Microsoft Prompts for Education - Students (GitHub)](https://github.com/microsoft/prompts-for-edu/tree/main/Students/Prompts)