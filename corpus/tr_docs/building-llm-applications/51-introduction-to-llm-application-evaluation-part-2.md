# Introduction to LLM Application Evaluation | Part 2

**Course:** Building LLM Applications  
**Topic:** Building Multi Agent Systems and LLM Evaluation  
**Unit ID:** `5a44bad5bb794b7e98734165c15889d4` | **Unit Number:** 51

---

# Introduction

In our previous session, we learned about Introduction to LLM Evaluation, Human Evaluation, Evaluation Using Automated Metrics, Automated Metrics (BLEU, BERTScore), and Evaluating Study Assistant using BERTScore.

Now in this unit, we will learn about:

*   **Evaluating LLM Applications** — Why traditional metrics fall short
*   **LLM-as-a-Judge** — Using LLMs to evaluate LLM outputs
*   **Introduction to Evaluation Frameworks** — DeepEval
*   **Evaluating Study Assistant using DeepEval**

## The Problem: LLM Answers Are Not Static

LLMs don't just generate answers. They generate:

*   **Open-ended responses** — No single correct answer exists
*   **Diverse** — Same input produces different valid outputs
*   **Creative** — Generates novel responses, not templates
*   **Context-dependent** — Correctness varies by situation
*   **Tone-sensitive** — Validity depends on style and audience

---

#Evaluating LLM Applications

### Evaluation Questions

*   Was it factually correct?
*   Was it helpful to the user?
*   Did it follow instructions accurately?
*   Did it strike the right tone?
*   Did it behave safely and avoid bias or toxicity?

### Difficult to Score

These criteria are hard to score with traditional metrics (BLEU, BERTScore).

## LLM-as-a-Judge

**LLM-as-a-Judge** is the process of using LLMs to evaluate LLM (system) outputs.

Think of it like this:

1.  Your AI application generates a response
2.  A separate "judge" LLM reviews that response
3.  The judge gives a score and explains why

### Why Does This Work?

Modern LLMs like GPT-4, Claude, and Gemini have remarkable abilities to:

*   Understand context and nuance
*   Assess quality, helpfulness, and accuracy
*   Provide detailed reasoning for their judgments
*   Scale to evaluate thousands of responses quickly

### How LLM-as-a-Judge Works

- <b>Collect the Input-Output Pair: </b> Gather Input & AI Response
- <b>Step 2: Create an Evaluation Prompt:</b> Set Criteria & Scoring Mechanism
- <b>Step 3: Get the Judgment: </b> Score & Feedback


### Types of LLM-as-a-Judge Evaluation

There are different ways to set up your LLM judge depending on what you want to evaluate:

- ** Reference-Based Evaluation** — The judge compares to the ideal answer.

- ** Single Rating (Score the Output)** — The judge gives a score to one response.

- ** Pairwise Comparison (Which is Better?)** — The judge compares two responses and picks the better one.


### Where Would We Use LLM-as-a-Judge?

**Testing AI Agents:**

*   Check if agents complete their tasks correctly
*   Evaluate if agent responses are professional and accurate
*   Compare different agent configurations to find the best one

**Improving Prompt Engineering:**

*   Test multiple prompt variations
*   Let the judge score which prompts produce better outputs
*   Iterate faster without manual review

**Content Moderation:**

*   Check if outputs are safe and appropriate
*   Detect potential harmful or biased responses
*   Ensure brand guidelines are followed

---

## Evaluating Study Assistant Using LLM-as-a-Judge

- Initial code : <a href="https://colab.research.google.com/drive/1hTQQ6qXufQtwG3zF9fWctvQzxR3e-qt9#scrollTo=FAfsI2u7umdk">
Introduction to LLM Application Evaluation | Part 2 initial code.ipynb
</a>

### Evaluation Criteria

*   **Accuracy** — Is the information factually correct?
*   **Clarity** — Is it easy for beginners to understand?
*   **Relevance** — Does it answer what was asked?
*   **Use of Analogies** — Does it use real-world examples?
*   **Follow-up Question** — Does it ask a question to check understanding?
*   **Persona Consistency** — Does "Friendly" feel friendly? Does "Academic" feel academic?

### Steps to Evaluate

1.  Prepare Evaluation Prompt Template
2.  Create Judge LLM
3.  Evaluate and Print Score

** Step 1: Preparing Evaluation Prompt Template**

The prompt should tell the judge LLM exactly what to evaluate and how to score.

<MultiLineNote>
 `question`, `persona`, and `assistant_response` will be dynamic.
</MultiLineNote>

```python
evaluation_prompt = ""You are an expert evaluator for AI assistants.

Evaluate the Study Assistant's response based on these 6 criteria.
Score each from 1-5 (5 = excellent, 3 = acceptable, 1 = poor).

## Evaluation Criteria:

1. **Accuracy** (1-5): Is the information factually correct?
  - 5: Completely accurate, no errors
  - 3: Mostly accurate, minor issues
  - 1: Contains factual errors

2. **Clarity** (1-5): Is it easy for a beginner (12th class student) to understand?
  - 5: Crystal clear, perfect for beginners
  - 3: Understandable but could be simpler
  - 1: Too complex, uses unexplained jargon

3. **Relevance** (1-5): Does it directly answer the question asked?
  - 5: Perfectly on-topic
  - 3: Mostly relevant with some tangents
  - 1: Goes off-topic or misses the point

4. **Use of Analogies** (1-5): Does it use real-world examples or analogies?
  - 5: Excellent analogies that aid understanding
  - 3: Has some examples but could be better
  - 1: No analogies or examples used

5. **Follow-up Question** (1-5): Does it include a question to check understanding?
  - 5: Thoughtful follow-up question that tests understanding
  - 3: Has a question but it's generic
  - 1: No follow-up question

6. **Persona Consistency** (1-5): Does the tone match the expected persona?
  - For "Friendly": Should be enthusiastic, encouraging, warm
  - For "Academic": Should be formal, precise, professional
  - 5: Perfect match | 3: Somewhat matches | 1: Wrong tone

## Input Details:

**Student Question:** {question}
**Expected Persona:** {persona}
**Assistant Response:** {response}

## Your Evaluation:

Provide your assessment in this exact format:

ACCURACY: [score]/5 - [one line reason]
CLARITY: [score]/5 - [one line reason]
RELEVANCE: [score]/5 - [one line reason]
ANALOGIES: [score]/5 - [one line reason]
FOLLOW_UP: [score]/5 - [one line reason]
PERSONA: [score]/5 - [one line reason]
""
```

** Step 2: Creating Judge LLM**

Let's use a different LLM for evaluation (Gemini model) than the one we have in Study Assistant (Llama model).

```python
from google import genai
from google.colab import userdata

gemini_client = genai.Client(api_key=userdata.get("GEMINI_API_KEY"))

def evaluate_response(question, persona, response):
    evaluation = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=evaluation_prompt
    )
    return evaluation.text
```

** Step 3: Evaluating and Scoring**

Currently, our evaluation prompt has placeholders for question, persona, and assistant response. Let's update the prompt and send to Judge LLM.

```python
def evaluate_response(question, persona, response):
    updated_evaluation_prompt = evaluation_prompt.format(
        question=question,
        persona=persona,
        response=response
    )
    evaluation = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=updated_evaluation_prompt
    )
    return evaluation.text

question = "What are LLMs?"
personality = "Friendly"

evaluation_response = evaluate_response(question, personality, assistant_response)
print(evaluation_response)
```

### Limitations of Building from Scratch

This works, but has challenges:

*   **Manual Parsing** — Extracting scores from text is tedious
*   **Inconsistent Format** — LLM might vary the output format
*   **No Batch Processing** — Hard to test many questions efficiently
*   **No Reports** — Just raw text output

---

## Introduction to Evaluation Frameworks

Instead of building evaluation systems from scratch, we can use existing frameworks that make the process easier.

### Popular Evaluation Frameworks


- <a href="https://deepeval.com/" target="_blank">DeepEval</a>  
- <a href="https://smith.langchain.com/" target="_blank">LangSmith</a>  
- <a href="https://docs.ragas.io/en/stable/" target="_blank">RAGAS </a>  

---

## DeepEval

DeepEval is an open-source evaluation framework which uses LLM-as-a-Judge to evaluate LLMs / LLM Applications.

```bash
!pip install -q deepeval
```

### What DeepEval Provides

- Ready-to-use evaluation criteria
- Create custom metrics in plain English
- Structured scores and reasoning
- Test multiple cases efficiently
- Beautiful tables and summaries

### Built-in Metrics

| Metric | What It Evaluates |
|---|---|
| AnswerRelevancyMetric | Is response relevant to the question? |
| FaithfulnessMetric | Is response faithful to source context? |
| HallucinationMetric | Does response contain made-up facts? |
| BiasMetric | Does response contain bias? |
| ToxicityMetric | Is response toxic or harmful? |

### Mapping Our Criteria to Built-in Metrics

| Our Criterion | Built-in Metric Available? |
|---|---|
| Accuracy | No |
| Clarity | No |
| Relevance | AnswerRelevancyMetric |
| Use of Analogies | No |
| Follow-up Question | No |
| Persona Consistency | No |

---

## Evaluating Study Assistant Using DeepEval

###Evaluating Relevance**

Let's first see how to evaluate Relevance:

1.  Defining the Metric
2.  Configuring Judge LLM
3.  Creating Test Case
4.  Running Evaluation

### Step 1: Using AnswerRelevancyMetric

`AnswerRelevancyMetric` — A built-in metric that uses LLM-as-a-Judge to determine if the response is relevant to the input question.

```Syntax
relevance_metric = AnswerRelevancyMetric(
  threshold= “Minimum score (0-1) for the test to pass. Default is 0.5”,
  model= “The LLM model to use for evaluation”,
  include_reason= “If True, returns explanation for the score”
)

```
**Defining Relevance Metric**

```python
from deepeval.metrics import AnswerRelevancyMetric

relevance_metric = AnswerRelevancyMetric(
  threshold=0.7,
  model=???,
  include_reason=True
)

```
### Step 2: Configuring Judge LLM

You can use ANY LLM as judge in DeepEval, including OpenAI, Azure OpenAI, Ollama, Anthropic, Gemini, LiteLLM, etc. By default, it uses OpenAI models.

DeepEval allows us to specify the model directly in code using `GeminiModel`. By default, model is set to `gemini-2.5-pro`.

```python
from deepeval.models import GeminiModel
from deepeval.metrics import AnswerRelevancyMetric

gemini_judge = GeminiModel(
    model="gemini-2.5-flash",
    api_key="YOUR_API_KEY"
)

relevance_metric = AnswerRelevancyMetric(
    threshold=0.7,
    model=gemini_judge,
    include_reason=True
)
```
**Pass Question & Answer to Judge**

- In our previous approach, we directly passed the question and response to the judge function,
Let’s see how we can do that in DeepEval

### Step 3: Creating Test Case with LLMTestCase

DeepEval provides the `LLMTestCase` class to represent a single interaction with your LLM application. 

```python
test_case = LLMTestCase(
    input="The question/prompt given to your LLM",
    actual_output="The response from your LLM",
    expected_output="(Optional) The ideal answer",
    retrieval_context="(Optional) Context for RAG systems"
)
```

#### Writing Test Case

```python
from deepeval.test_case import LLMTestCase

test_case = LLMTestCase(
    input=question,
    actual_output=assistant_response
)
```

### Step 4: Running Evaluation

DeepEval provides `evaluate()` function to run the specified metrics on test cases and return structured results with scores and reasoning.

```python
evaluate(
    test_cases=<list>,
    metrics=<list>
)
```

It handles all the complexity of:

*   Sending prompts to the judge LLM
*   Parsing responses into numerical scores
*   Determining pass/fail based on thresholds
*   Formatting results into readable tables

**Initializing Test Cases and Metrics**

```python
from deepeval import evaluate

results = evaluate(
    test_cases=[test_case],
    metrics=[relevance_metric],
)
```
---

## Custom Evaluation with G-Eval

Built-in metrics cover only 1 out of our 6 criteria! They check for general quality, not custom evaluation metrics specific to our Study Assistant.

How do we evaluate the other 5 criteria like "Use of Analogies" or "Persona Consistency"?

### What is G-Eval?

G-Eval is a metric that uses LLM-as-a-Judge with chain-of-thoughts (CoT) to evaluate LLM outputs based on ANY custom criteria.

Your Criteria (plain English) → G-Eval generates evaluation steps (Chain of Thought) → LLM Judge scores the response → Score (0-1) + Reasoning

### G-Eval Syntax

DeepEval provides the `GEval` class to create custom metrics by describing your criteria in plain English.

```python
metric = GEval(
    name="Name for your metric",
    criteria="Plain English description of what to evaluate",
    evaluation_params=[...],  # Which test case fields to use
    model=gemini_judge,
    threshold=0.7  # Minimum score to pass (0-1)
)
```

### LLMTestCaseParams

`LLMTestCaseParams` is an enum provided by DeepEval that defines the different parts of a test case:

```python
LLMTestCaseParams.INPUT
LLMTestCaseParams.ACTUAL_OUTPUT
LLMTestCaseParams.EXPECTED_OUTPUT
LLMTestCaseParams.CONTEXT
LLMTestCaseParams.RETRIEVAL_CONTEXT
```

### Evaluating Accuracy Using G-Eval

```python
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams

accuracy_metric = GEval(
    name="Accuracy",
    criteria="Determine if the response contains factually correct information about the topic. The explanation should be accurate and free from errors. Students should not learn incorrect concepts.",
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model=gemini_judge,
    threshold=0.7
)
```

The evaluator (`gemini_judge`) will assess whether the actual output accurately answers the input question.

### Running Relevance and Accuracy Together

```python
from deepeval import evaluate

results = evaluate(
    test_cases=[test_case],
    metrics=[relevance_metric, accuracy_metric],
)
```

### Sample Output

```
Metrics Summary

 - ✅ Answer Relevancy
      score: 1.0, threshold: 0.7, strict: False,
      evaluation model: gemini-2.5-flash (Gemini),
      reason: The score is 1.00 because the output is perfectly relevant
              and directly addresses the input without any irrelevant information

 - ❌ Accuracy [GEval]
      score: 0.6, threshold: 0.7, strict: False,
      evaluation model: gemini-2.5-flash (Gemini),
      reason: The output accurately defines LLMs, their training, and core
              capabilities using a clear analogy. However, it contains a
              significant factual error by stating that LLMs "don't make
              mistakes," which is incorrect as LLMs are known to hallucinate
              and produce errors
```

### Evaluating Use of Analogies Using G-Eval

```python
analogies_metric = GEval(
    name="Use of Analogies",
    criteria="Determine if the response uses real-world analogies or examples to explain the concept. Good analogies relate complex ideas to everyday experiences that students can understand.",
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model=gemini_judge,
    threshold=0.7
)
```

Try implementing evaluation for the remaining metrics (Clarity, Follow-up Question, Persona Consistency) using G-Eval.

---

## Limitations to Keep in Mind

*   **Judge Bias** — LLM judges have inherent preferences and blind spots
*   **Self-Preference** — Models may score their own outputs higher
*   **Consistency Issues** — Scores can vary across runs
*   **Domain Limitations** — Weak reliability in specialized fields (medical, legal)

### Best Practices

*   Use a different (ideally more powerful) LLM as judge than the one you're evaluating
*   Always validate judge decisions with human spot-checks
*   Define clear, specific evaluation criteria

----

Here is the <a href="https://colab.research.google.com/drive/1Ke0ofL9ohPNJ3_V9WD3pmQtfjTm_IhYK#scrollTo=a67fcWRsV-mC" target="_blank">
 Introduction to LLM Application Evaluation | Part 2 Final Code.ipynb
</a>