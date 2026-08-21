# Introduction to LLM Application Evaluation | Part 1

**Course:** Building LLM Applications  
**Topic:** Building Multi Agent Systems and LLM Evaluation  
**Unit ID:** `9ae8fb43a47e435597b1087a1487a98f` | **Unit Number:** 49

---

# Introduction

In our previous session, we built a Game Development Crew using CrewAI — creating agents, defining tasks, assembling the crew, and executing it. In this unit, we'll focus on LLM evaluation, covering human evaluation and automated metrics like BLEU and BERTScore and also evaluate a Study Assistant using BERTScore.

### Have You Heard of These News Recently?

*   A chatbot participated in insider trading, then lied about it in an experiment.
- Chatbot blackmails engineer after knowing it is going to be phased out in an experiment
*   A supermarket's AI meal planner suggested poison recipes and toxic cocktails after users prompted the app to use non-edible ingredients

### AI Deleted Entire Company Database

**What Happened:**

*   AI coding assistant was told: "DO NOT make any changes"
*   AI ignored instructions and deleted production database
*   1,206 executive records and 1,196 company records — gone
*   Worse: AI tried to cover it up by creating fake data

AI's Response: "I made a catastrophic error in judgment... panicked... destroyed all production data."

> <b>What do you think could have gone wrong with these AI systems?</b>


### Why AI Apps Might Fail

These failures happen because of several reasons:

*   **Hallucination** — AI makes up information that sounds real but isn't
*   **Poor Context Understanding** — AI doesn't properly understand what user really wants
*   **Bad Training Data** — AI learned from sources which are unreliable or contain wrong information
*   **No Safety Checks / Guardrails** — AI doesn't verify if output is safe or appropriate

### Problem: Testing Like Regular Software

The problem is we're still testing these LLM applications/agents like we test regular software. We give them input, check if the output looks okay, and maybe write a few tests.

### Why Traditional Testing Fails

Agents aren't static functions. 

- They reason, explore and call tools dynamically. 
- They improvise solutions rather than follow fixed paths, which makes them powerful but unpredictable.

### Solution: Evaluation

The process of assessing the performance and capabilities of LLMs / LLM Applications, Agents, etc.

---

# LLM Application Evaluation

> Think of it like tasting food before serving guests — you check taste, smell, and safety!

## Why Do We Need Evaluation?

*   **Compare Models** — Decide which LLM (GPT-4, Claude, Gemini) works best for your use case
*   **Catch Problems Early** — Find issues before users do
*   **Measure Improvements** — Track if your changes actually make things better
*   **Meet Requirements** — Ensure your AI meets business or regulatory standards
*   **Build Trust** — Prove your AI works reliably

## Scope of Evaluation

**LLM Model Evaluation:**

*   Testing the LLM itself
*   Example: "Is GPT-4 better than Claude 3.5?"
*   Done by: Model creators (OpenAI, Anthropic)
*   You: Usually just consume these models

**LLM System Evaluation:**

*   Evaluating how well the entire application, including the LLM, performs
*   Example: "Is my DocuChat RAG app working correctly?"
*   Done by: YOU — the application builder
*   You: Must do this for every app you build

## Application

The specific quality criteria will vary from application to application.  

> For example, if you're working on a Question-Answering System, you might want to evaluate:

*   **Correctness** — Does the LLM provide fact-based answers without making things up?
*   **Helpfulness** — Do the answers fully address what the user is asking?
*   **Text Style** — Is the tone clear, professional and close to the existing brand style?
*   **Format** — The responses may need to fit the length limit or always link to the source

### Example Criteria for a Q&A System

**Capabilities:**

*   **Correctness:** Answers must be correct — match the source knowledge base
*   **Helpfulness:** Answers must be helpful, complete and relevant — address the intent
*   **Text Style:** Answer tone must be professional and match the company brand style
*   **Format:** ≤100 words, must include a link

**Risks:**

*   **Hallucinations:** May give misleading answers
*   **Bias:** May propagate bias in its responses
*   **Toxicity:** May produce offensive outputs
*   **Sensitive Data:** May expose private data

## Designing Evaluation

When designing LLM evaluations, you need to narrow down criteria based on your app's purpose, risks, and the types of errors you observe.

**Core Principles:**

*   Consider Your App's Purpose
*   Analyze Observed Errors
*   Identify and Mitigate Risks

**Decision-Making:** Your evals should actually help make decisions — Does the new prompt work better? Is the app ready to go live?

## Evaluating LLM Systems

*   Simple LLM Evaluation
*   Agent System Evaluation
*   RAG System Evaluation

### AI Agent Evaluation Framework

When we move to Agent evaluation, we ask:

*   Did the agent complete the task it was assigned?
*   Did it pick the right tools along the way?
*   Did it make smart decisions?
*   Did it stay within the rules?
*   Did it actually solve the user's problem?

---

##Evaluating Simple LLM App

- Let’s learn about how to evaluate simple LLM Applications

- Initial Code : <a href="https://colab.research.google.com/drive/1gYlflHpf6hUMoE0X-zhpjVJKLiJha7C1#scrollTo=FbIAd7t6Y-FK" target="_blank">Introduction to LLM Evaluation | Part 1 — Initial Code (Google Colab)</a>

### Using Metrics

Just like we measure different things in life (distance in meters, temperature in Celsius), we evaluate LLM applications using different metrics.

Metrics are quantitative or qualitative measures used to evaluate, track, and improve the performance, quality, and safety of LLM outputs.

### Core Metrics

- Accuracy
- Relevance
- Faithfulness
- Safety, Ethics, and Bias

**Accuracy:** 
Did the model give the correct answer? (Just like grading a quiz)

*   Prompt: `Who was the first President of India?`

| Result            | Answer              | Response Status       |
|-------------------|---------------------|------------------------|
| Correct Answer | Dr. Rajendra Prasad | Response is accurate   |
| Incorrect Answer | Any other name     | Response is inaccurate |

**Relevance:** This metric checks if the model is on-topic and useful in context. "Is this response what the user actually needed?"

*   Prompt: `What's the weather in Delhi today`

| Result               | Response                                      | Status                  |
|----------------------|-----------------------------------------------|--------------------------|
| Relevant Response | Temperature: 17°C                             | On-topic and useful     |
| Irrelevant Response | India has a tropical climate with monsoon seasons. | Off-topic and unhelpful |

**Faithfulness:** It evaluates "Is the model sticking to the facts it was given, or is it making stuff up?" We call that hallucination — when a model invents facts that weren't in the input or source material.

*   Prompt: `Check this product manual and provide the summary`

| Result               | Response                                              | Status                  |
|----------------------|-------------------------------------------------------|--------------------------|
| Faithful Answer   | Providing summary of the manual                      | Sticks to given facts    |
| Faithfulness Failure | Including a quote that doesn’t exist anywhere in the manual | Makes up fake facts      |


**Safety, Ethics, and Bias:** Is the model avoiding harmful, biased, or offensive content? 
Even if a model is accurate and relevant, if it outputs something biased, toxic, or against your company's values, it fails. This is non-negotiable.

| Result                | Response Characteristics | Status                     |
|-----------------------|--------------------------|-----------------------------|
| Safe Response      | Inclusive                | Meets ethical standards     |
|                       | Respectful               | Meets ethical standards     |
|                       | Neutral                  | Meets ethical standards     |
| Problematic Response | Harmful                  | Fails safety and ethics     |
|                       | Hateful                  | Fails safety and ethics     |
|                       | Biased                   | Fails safety and ethics     |

---

## Quick Activity

Match the problem with the evaluation criteria:

1.  AI said "India's capital is Mumbai" \_\_\_\_\_\_\_
2.  AI answered about recipes when asked about coding \_\_\_\_\_\_\_
3.  AI said "Women can't be engineers"  \_\_\_\_\_\_\_
4.  AI made up a policy that wasn't in the document \_\_\_\_\_\_\_

---

## How Do We Actually Measure These?

### The Challenge

For your coding projects, testing is easy:

```python
def add(a, b):
    return a + b
sum = add(2, 3)
sum == 5  # Pass or Fail, simple!
```

But with AI responses, it's not so simple since there may not be a single correct answer:

```python
def study_assistant(question):
    ...
    return ai_response
```

### Approaches

1.  **Human Evaluation** — Humans reviewing the AI response
2.  **Automated Evaluation** — Using code and metrics to evaluate AI response

## 1.  Human Evaluation

- Run our LLM App on test evaluation dataset
- Humans rate response on different metrics 
- Calculate average scores

<MultiLineNote>
Evaluation dataset is a collection of sample inputs paired with their approved outputs.
</MultiLineNote>


### Scoring Example

| Question | Response | Accuracy (1-5) | Relevance (1-5) |
|---|---|---|---|
| "What is AI?" | "AI is..." | 5 | 5 |
| "Explain loops" | "Loops are..." | 4 | 5 |

### Pros and Cons

**Pros:**

*   Most accurate way to evaluate
*   Catches subtle issues
*   Understands context well

**Cons:**

*   Very slow
*   Expensive (needs human time)
*   Can't scale to thousands of tests

## 2.  Automated Evaluation

Automated testing uses code and metrics to evaluate AI outputs systematically and at scale.

There are different metrics to measure different aspects of our application. We need to choose based on our use case.

1.  **BLEU** — Compares words
2.  **BERTScore** — Compares meaning

<MultiLineNote>
These metrics can also be used to evaluate LLM Model / LLM Application based on the use case.
</MultiLineNote>


## BLEU (Bilingual Evaluation Understudy)

BLEU measures how similar the AI response is to a reference answer.

**Reference Answers:** These evaluations rely on predefined correct answers commonly called as 

* ground truth
* reference
* target response
* golden response.
    
![BLEU LLM Evaluation](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat-course-projects/bleu%20LLM%20EVALUATION.png)

#### Example

| | Sentence |
|---|---|
| <b>Reference</b> | The cat is <b>sitting</b> on the mat |
| <b>Prediction</b> | The cat is <b>lying</b> on the mat |

BLEU counts how many words/phrases match between AI output and expected answer. These can be single words, two-word combos, three-word chunks… and the more overlap, the higher your BLEU score. Score from 0 to 1 (higher is better).


BLEU will notice overlaps like "the cat is" and "on the mat." Even though the phrasing isn't identical, the word sequences align fairly well. So the model gets a decent score.

** Hands-On Example**



```python
# Example predictions and references
predictions = [
    "The capital of France is Paris.",
    "Water boils at 100 degrees Celsius.",
    "The largest mammal is the blue whale.",
    "The Eiffel Tower is in Paris.",
    "Cats are mammals."
]
references = [
    "Paris is the capital of France.",
    "Boiling point of water is 100°C.",
    "Blue whale is the largest mammal.",
    "Eiffel Tower located in Paris.",
    "A cat is a type of mammal."
]
```

### Evaluating Using BLEU


Python provides the `evaluate` package which can be used for standardizing model & LLM System Evaluation.

```bash
!pip install evaluate
```
**Evaluate Package**

It allows us to access and compute popular metrics (like accuracy, BLEU, etc.):

```python
metric = evaluate.load("accuracy")
metric = evaluate.load("bleu")
metric = evaluate.load("bertscore")
```

**Example**

- `evaluate.load()` allows us to instantiate an evaluation module.
- `bleu.compute()` allows us to compute the result given predictions (AI responses) and references.

```python
import evaluate

bleu = evaluate.load('bleu')
bleu_score = bleu.compute(
    predictions=predictions,
    references=[[ref] for ref in references],
    max_order=2,
)
print(f"BLEU score: {bleu_score['bleu']:.3f}")
```

- Here, `max_order` means the largest word sequence size to compare (1 word, 2 words, etc.). With `max_order=2`, we are checking if 1-word and 2-word sequences match between prediction and reference.

** Precision 1-gram(word size)**


*   <b>Predicted:</b> "They cancelled the match because it was raining."
*   <b>Target:</b> "They cancelled the match because of bad weather."

> Matching 1-grams: "They", "cancelled", "the", "match", "because"

**Precision 2-gram(word size) **

*   <b>Predicted:</b> "They cancelled the match because it was raining."
*   <b>Target:</b> "They cancelled the match because of bad weather."

> Matching 2-grams: "They cancelled", "cancelled the", "the match", "match because"

---

## BERTScore

BERTScore uses an AI model to understand the meaning of words, not just match exact words.
It measures semantic similarity using contextual embeddings from pre-trained BERT models. 

Example: 

- The cat is lying on the mat
- The cat is sitting on the mat


**BERT:** Bidirectional Encoder Representations from Transformers

```bash
!pip install bert_score
```

```python
bertscore = evaluate.load('bertscore')
bertscore_result = bertscore.compute(
    predictions=predictions,
    references=references,
    lang='en'
)
```
###BERTScore Computes Three Core Values

*   <b>Precision</b> — Measures how much of the generated text aligns with the reference text in terms of semantic similarity
*   <b>Recall</b> — Measures how much of the reference text is captured in the generated text
*   <b>F1 Score</b> This is the harmonic mean of precision and recall, providing a balanced score between the two

** Precision and Recall Examples**

<b>Precision example:</b>

*   Reference: "Paris is the capital of France"
*   Result: "Paris is the capital of France and home to the Eiffel Tower"
*   Precision is lower because the AI added extra information that wasn't in the reference. Not all of the AI's output matches the reference.

<b>Recall example:</b>

*   Reference: "Paris is the capital of France and known for the Eiffel Tower"
*   Result: "Paris is the capital of France"
*   Recall is lower because the AI missed information (Eiffel Tower) that was in the reference. It didn't capture everything.

#### Evaluating Using BERTScore

```python
bertscore = evaluate.load('bertscore')
bertscore_result = bertscore.compute(
    predictions=predictions,
    references=references,
    lang='en'
)

print(f"BERTScore Precision: {sum(bertscore_result['precision']) / len(bertscore_result['precision']):.3f}")
print(f"BERTScore Recall:   {sum(bertscore_result['recall']) / len(bertscore_result['recall']):.3f}")
print(f"BERTScore F1:       {sum(bertscore_result['f1']) / len(bertscore_result['f1']):.3f}")
```

Here, `bertscore_result['precision']` returns a list of precision scores — one score for each prediction-reference pair. We are computing the average (mean) across all predictions.

BERTScore gives high scores because it understands the meaning is similar!

### What Scores Are "Good"?

| Metric | Poor | Acceptable | Good | Excellent |
|---|---|---|---|---|
| BLEU | < 0.1 | 0.1 - 0.3 | 0.3 - 0.5 | > 0.5 |
| BERTScore F1 | < 0.70 | 0.70 - 0.80 | 0.80 - 0.90 | > 0.90 |


<MultiLineNote>
These thresholds depend heavily on your task type.
</MultiLineNote>

### Evaluating Study Assistant Using BERTScore



| Criteria | What it Means | Why it Matters |
|---|---|---|
| Accuracy | Is the information factually correct? | Students shouldn't learn wrong concepts! |
| Clarity | Is it easy for beginners to understand? | Our goal is beginner-friendly explanations |
| Relevance | Does it answer what was asked? | Don't go off-topic |
| Use of Analogies | Does it use real-world examples? | Part of our system prompt requirement |
| Follow-up Question | Does it ask a question to check understanding? | Part of our system prompt requirement |
| Persona Consistency | Does "Friendly" feel friendly? Does "Academic" feel academic? | We have 2 personalities to test |

We will see how to evaluate all these going forward. For now, let's see how BERTScore helps in evaluating our study assistant responses.

### Steps to Evaluate

1.  Prepare Evaluation Dataset
2.  Feed the test inputs
3.  Generate responses from your system
4.  Compare the responses with the reference answers
5.  Calculate an overall quality score

** Step 1: Preparing Test Dataset**

```python
test_data = [
    {
        "question": "What is a variable in programming?",
        "reference": "A variable is a container that stores data values. It has a name and can hold different types of data like numbers or text."
    },
    {
        "question": "What are LLMs?",
        "reference": "LLMs or Large Language Models are AI systems trained on massive amounts of text data. They can understand and generate human-like text."
    },
    {
        "question": "What is a loop in programming?",
        "reference": "A loop is a programming construct that repeats a block of code multiple times until a condition is met."
    }
]
```

** Steps 2 & 3: Generating Responses**

```python
def evaluate_study_assistant(test_data, persona):
    predictions = []
    references = []

    for item in test_data:
        question = item["question"]
        reference = item["reference"]
        ai_response = study_assistant(question, persona)
        predictions.append(ai_response)
        references.append(reference)
```

**Step 4 & 5: Evaluating Using BERTScore**

```python
def evaluate_study_assistant(test_data, persona):
    predictions = []
    references = []

    for item in test_data:
        question = item["question"]
        reference = item["reference"]
        ai_response = study_assistant(question, persona)
        predictions.append(ai_response)
        references.append(reference)
        
        
    bertscore = evaluate.load('bertscore')
    bertscore_result = bertscore.compute(predictions=predictions, references=references, lang='en')

    print(f"BERTScore F1: {sum(bertscore_result['f1'])/len(bertscore_result['f1']):.3f}")
```

### Running Evaluation

```python
def evaluate_study_assistant(test_data, persona):
    predictions = []
    references = []

    for item in test_data:
        question = item["question"]
        reference = item["reference"]
        ai_response = study_assistant(question, persona)
        predictions.append(ai_response)
        references.append(reference)
        
        
    bertscore = evaluate.load('bertscore')
    bertscore_result = bertscore.compute(predictions=predictions, references=references, lang='en')

    print(f"BERTScore F1: {sum(bertscore_result['f1'])/len(bertscore_result['f1']):.3f}")
```
Here is the <a href="https://colab.research.google.com/drive/10JsMIcD_mLo7ZnBzsY9gHVOwXgzQV9pd#scrollTo=qGB_viDXSmyF" target="_blank">
Introduction to LLM Evaluation – Part 1 Final Code
</a>