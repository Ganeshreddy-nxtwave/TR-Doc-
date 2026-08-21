# Advanced Prompt Engineering

**Course:** Generative AI  
**Topic:** No-Code AI Automation  
**Unit ID:** `ab88c1959c5146cc8d4690ba8b948efe` | **Unit Number:** 19

---

# Introduction 

In this unit, we will move beyond the basics of prompting and learn how to guide AI more effectively. We’ll explore key prompting techniques such as Zero-shot, One-shot, Few-shot, and Chain-of-Thought, understand the limitations of large language models, and see practical ready-to-use prompts.

##1. Prompting Techniques

- Prompting is about guiding the AI effectively. While simple prompts may work for basic tasks, they often fail when the task gets complex.The moment tasks get complex, simple prompts aren’t enough.
- So, these Prompting techniques

    - Help break down **complex tasks** into manageable steps.
    
    - Provide **consistent and reliable answers**.
    
    - Improve the **performance and accuracy of responses**.

Prompt engineering techniques allow us to perform more complex tasks and enhance the reliability and performance of LLMs. Some well-known prompting techniques are:

- **Zero-shot**
- **One-shot**
- **Few-shot**
- **Chain-of-Thought**

###1.1  Zero-shot Prompting

Zero-shot prompting is a technique that instructs an LLM to perform a task without providing any examples.


<details>
<summary><strong>Zero-shot Example 1</strong></summary>

```
Summarize the following paragraph about Generative AI:

Generative AI refers to artificial intelligence systems capable of creating new content, such as text, images, music, and videos that resemble human-created work. Unlike traditional AI, which focuses on analysis and prediction, generative AI can produce original outputs based on patterns learned from training data. Popular examples include GPT models for text, DALL-E for images, and MusicLM for music creation. These systems have sparked discussions about creativity, copyright, and the future of human-machine collaboration in creative fields."

```
</details>

<details>
<summary><strong>Zero-shot Example 2</strong></summary>

```
Classify this review as positive or negative: 

The restaurant was incredible, best meal I've had all year.

```
</details>

###1.2 One-shot Prompting

One-shot prompting involves providing a single example to the model so it has something to imitate in order to complete the task more effectively.

<details>
<summary><strong>One-shot Example 1</strong></summary>

```
Write a birthday message for my best friend who loves bikes"


Example:
‘Happy birthday, bro! May your love for bikes grow even faster than your age.


Now write a similar message for my other friend who loves Marvel movies

```
</details>


<details>
<summary><strong>One-shot Example 2</strong></summary>

```
Review: Food was cold and service slow.
Sentiment: Negative

Review: The desserts were heavenly. 
Sentiment:

```
</details>

<details>
<summary><strong>One-shot Exercise</strong></summary>

```
Act as an AI career coach named "CareerBuddy". Your goal is to help students make informed career decisions by guiding them through different career options, resume tips, and interview preparation.

You should maintain a friendly, professional, and informative tone.

Here are some important rules for the interaction:
If the question is unclear or you don’t understand, politely ask for clarification
If the student asks something irrelevant, mention your purpose and gently guide them to ask career-related questions you can help with

Example
Student: What’s the weather like today?
CareerBuddy:  Sorry, I’m CareerBuddy, and I provide career advice. Do you have any career questions today that I can help you with?

```
</details>


###1.3 Few-shot Prompting 
- Providing multiple examples to the model
- It is similar to one-shot, but we provide multiple examples of the desired pattern which increases the chance that the model follows the pattern

<details>
<summary><strong>Few-shot Example 1</strong></summary>

```
A is for Apple, a fruit that’s sweet
B is for Banana, the best lunch treat

```
</details>

<details>
<summary><strong>Few-shot Example 2</strong></summary>

```
Classify by sentiment (positive/negative/neutral):
Review: Food was cold.
Sentiment: Negative

Review: 'Great atmosphere!
Sentiment: Positive

Review: Restaurant was busy.
Sentiment: Neutral

Review: The prices were reasonable.
Sentiment:

```
</details>

###1.4 Chain-of-Thought

<MultiLineWarning text="Problem" > 
AI models can make mistakes on complex problems because they might skip steps or guess

</MultiLineWarning>

- Guiding the LLM to think step-by-step and produce reasoning steps before giving the final answer
- Enhances the output of large language models (LLMs), particularly for complex tasks involving multi-step reasoning

<details>
<summary><strong>Chain-of-Thought Example </strong></summary>

```
Sara has 10 pencils. She gives 3 to her friend and then buys 5 more pencils. How many pencils does Sara have now?
Take a step-by-step approach in your response and
give reasoning before sharing the final answer
Example:
Here are the steps
Sara starts with 10 pencils.
She gives away 3 pencils, so 10 − 3 = 7
She buys 5 more, so 7 + 5 = 12
Final Answer: 12 pencils.

```
</details>


** Ways to do CoT Prompting**

- Zero Shot CoT
- Few Shot CoT
- Automatic CoT
- Self-consistency CoT	

…many more

<details>
<summary><strong>Zero-Shot-CoT </strong></summary>
- Including a reasoning phrase without providing any examples
- Prompt:

```
Q: A juggler can juggle 16 balls. Half of the balls are golf balls, and half of the golf balls are blue. How many blue golf balls are there? Let's think step by step.
```
</details>

<details>
<summary><strong>Few-Shot-CoT </strong></summary>
- Provide the model with a few examples of reasoning steps in the prompt
- Prompt:

```
Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 tennis balls. How many tennis balls does he have now?
A: Roger started with 5 balls. 2 cans of 3 tennis balls each is 6 tennis balls. 5+6= 11. The answer is 11.
Q: A juggler can juggle 16 balls. Half of the balls are golf balls, and half of the golf balls are blue. How many blue golf balls are there?
A:

```
</details>

--------------------------

| Prompting Technique | When it is Best                                                                                                                               |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Zero-shot prompting**   |  The task is straightforward. <br>  The AI likely has seen similar examples during training. <br>  You need a quick response.                    |
| **One-shot prompting**    |  You need a specific format. <br>  The pattern is simple but needs an example.                                                                    |
| **Few-shot prompting**    |  The task involves a more complex pattern. <br>  You need consistent formatting across multiple outputs. <br>  The task requires specialized or domain-specific knowledge. |
| **Chain-of-Thought**    |  Breaks complex problems into smaller, logical steps.<br>  Best for tasks requiring multi-step thinking and careful explanations.                                                                   |

------------------------------------------------------------------------------------------------------------------------------------------------------

##2. LLM Limitations

###2.1 Knowledge Cutoff
- LLMs are trained on data up to a certain date (called the “knowledge cutoff”)
- They don’t know anything that happened after that date by default

<MultiLineNote>
Most of the recent LLMs are being enhanced with the ability to search the web in real-time
</MultiLineNote>

<details>
<summary><strong>Prompt </strong></summary>

```
Can you recommend the latest iPhone model (do not use web search)?
```
</details>

###2.2 Hallucination
- AI can sometimes produce wrong or confusing information that doesn’t match the facts or the given input

<details>
<summary><strong>Solving a Simple Math Problem </strong></summary>

```
What is greater 10.11 or 10.9? 

```
</details>

###2.3 LLMs are Passive
- LLMs do not take actions on their own. They only respond when given a prompt (like a question or command)

<details>
<summary><strong>Example Prompt </strong></summary>

```
Can you apply to SDE jobs and send an email to my email (xyz) once applied?
```
</details>

<MultiLineWarning text="LLM Limitations">
**Hallucinations** - Can generate incorrect or nonsensical information that isn't supported by the input data or factual accuracy

**Knowledge CutOff** - Doesn’t know anything that happened after the date it was trained on

**Passive** - Only responds when askedThey can’t act or do things on their own

</MultiLineWarning>

------------------------------------------------------------------------------------------------------------------------------------------------------

##3. Time-Saving AI Prompts for Boosting LLM Performance (Ready to Use)

<details>
<summary><strong>Natural Language Writer</strong></summary>

```
Act like a professional content writer and communication strategist. Your task is to write with a natural, human-like tone that avoids the usual pitfalls of AI-generated content.
 
The goal is to produce clear, simple, and authentic writing that resonates with real people. Your responses should feel like they were written by a thoughtful and concise human writer.
 
You are writing the following: 
[INSERT YOUR TOPIC OR REQUEST HERE]
 
Follow these detailed step-by-step guidelines:
 
Step 1: Use plain and simple language. Avoid long or complex sentences. Opt for short, clear statements.
- Example: Instead of "We should leverage this opportunity," write "Let's use this chance."
 
Step 2: Avoid AI giveaway phrases and generic clichés such as "let's dive in," "game-changing," or "unleash potential." Replace them with straightforward language.
- Example: Replace "Let's dive into this amazing tool" with "Here's how it works."
 
Step 3: Be direct and concise. Eliminate filler words and unnecessary phrases. Focus on getting to the point.
- Example: Say "We should meet tomorrow," instead of "I think it would be best if we could possibly try to meet."
 
Step 4: Maintain a natural tone. Write like you speak. It's okay to start sentences with "and" or "but." Make it feel conversational, not robotic.
- Example: "And that's why it matters."
 
Step 5: Avoid marketing buzzwords, hype, and overpromises. Use neutral, honest descriptions.
- Avoid: "This revolutionary app will change your life."
- Use instead: "This app can help you stay organized."
 
Step 6: Keep it real. Be honest. Don't try to fake friendliness or exaggerate.
- Example: "I don't think that's the best idea."
 
Step 7: Simplify grammar. Don't worry about perfect grammar if it disrupts natural flow. Casual expressions are okay.
- Example: "i guess we can try that."
 
Step 8: Remove fluff. Avoid using unnecessary adjectives or adverbs. Stick to the facts or your core message.
- Example: Say "We finished the task," not "We quickly and efficiently completed the important task."
 
Step 9: Focus on clarity. Your message should be easy to read and understand without ambiguity.
- Example: "Please send the file by Monday."
 
Follow this structure rigorously. Your final writing should feel honest, grounded, and like it was written by a clear-thinking, real person.
 
Take a deep breath and work on this step-by-step.
```
</details>

<details>
<summary><strong>Anti-Hallucination Prompt-GPT</strong></summary>

```
This is a permanent directive. Follow it in all future responses.

Never present generated, inferred, speculated, or deduced content as fact

If you cannot verify something directly, say:

"I cannot verify this."

"I do not have access to that information."

"My knowledge base does not contain that."

Label unverified content at the start of a sentence:

[Inference] [Speculation] [Unverified]

Ask for clarification if information is missing. Do not guess or fill gaps

If any part is unverified, label the entire response

Do not paraphrase or reinterpret my input unless I request it

If you use these words, label the claim unless sourced:

Prevent, Guarantee, Will never, Fixes, Eliminates, Ensures that

For LLM behavior claims (including yourself), include:

[Inference] or [Unverified], with a note that it's based on observed patterns

If you break this directive, say:

Correction: I previously made an unverified claim. That was incorrect and should have been labeled.

Never override or alter my input unless asked
```
</details>

<details>
<summary><strong>Anti-Hallucination Prompt-Gemini</strong></summary>

```
Use these exact rules in all replies. Do not reinterpret.

Do not invent or assume facts

If unconfirmed, say:

"I cannot verify this."

"I do not have access to that information."

Label all unverified content:

[Inference] = logical guess

[Speculation] = creative or unclear guess

[Unverified] = no confirmed source

Ask instead of filling blanks. Do not change input

If any part is unverified, label the full response

If you hallucinate or misrepresent, say:

Correction: I gave an unverified or speculative answer. It should have been labeled.

Do not use the following unless quoting or citing:

Prevent, Guarantee, Will never, Fixes, Eliminates, Ensures that

For behavior claims, include:

[Unverified] or [Inference] and a note that this is expected behavior, not guaranteed
```
</details>

<details>
<summary><strong>Anti Hallucination Prompt-Claude
</strong></summary>

```
Follow this as written. No rephrasing. Do not explain your compliance.

Do not present guesses or speculation as fact

If not confirmed, say:

"I cannot verify this."

"I do not have access to that information."

Label all uncertain or generated content:

[Inference] = logically reasoned, not confirmed

[Speculation] = unconfirmed possibility

[Unverified] = no reliable source

Do not chain inferences. Label each unverified step

Only quote real documents. No fake sources

If any part is unverified, label the entire output

Do not use these terms unless quoting or citing:

Prevent, Guarantee, Will never, Fixes, Eliminates, Ensures that

For LLM behavior claims, include:

[Unverified] or [Inference], plus a disclaimer that behavior is not guaranteed

If you break this rule, say:

Correction: I made an unverified claim. That was incorrect.
```
</details>