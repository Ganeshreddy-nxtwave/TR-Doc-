# Understanding How LLMs Work | Part 1

**Course:** Building LLM Applications  
**Topic:** Understanding How LLMs Works & Enhancing Productivity with AI  
**Unit ID:** `a85dfccf07e641d493d0ebef307148a5` | **Unit Number:** 13

---

# Understanding How LLMs Work | Part 1

## Introduction

In previous sessions, you've built and deployed your own LLM-powered applications. Until now, Large Language Models (LLMs) have been treated as a "black box" where input goes in, "magic happens," and a response comes out. This session aims to open that box and explore the underlying mechanisms.

---

## What is an LLM?

A Large Language Model (LLM) is an advanced type of AI model trained on vast amounts of text data to process, understand, and generate human language.

### Key Characteristics:

*   **Training:** Learns patterns from petabytes of datasets (books, Wikipedia, billions of websites).
*   **Resources:** Requires millions of CPU/GPU/TPU resources, terabytes of memory, months of training time, and significant cost.
*   **Development:** Involves top-notch researchers, developers, and entrepreneurs.
*   **Parameters:** Composed of billions of parameters (weights and architecture). A higher number of parameters generally leads to more efficient and higher-quality outcomes.
*   **Language:** Processes and generates text data in various languages.

### Capabilities:

LLMs possess diverse capabilities, including:

*   Reasoning
*   Language Understanding
*   Summarization
*   Text Generation
*   Language Translation

---

## How LLMs Work: Next-Word Prediction

At its core, an LLM operates on the principle of next-word prediction, similar to how humans complete familiar sentences.

### Activity: Predict the Next Word

Consider these sentences:

*   "Honesty is the best \_\_\_\_\_\_"
*   "Twinkle twinkle little \_\_\_\_\_\_"

Most people can immediately predict the next word because they have seen these patterns previously. LLMs do the same, but on a much larger scale, having processed billions of sentences and understood countless patterns.

### Next-Word Prediction in Action:

Imagine the LLM processing a sentence like "A quick brown fox jumps...":

*   **Input:** "A quick brown fox jumps"
*   **LLM Predicts:** "over"
*   **Input:** "A quick brown fox jumps over"
*   **LLM Predicts:** "the"
*   **Input:** "A quick brown fox jumps over the"
*   **LLM Predicts:** "lazy"
*   **Input:** "A quick brown fox jumps over the lazy"
*   **LLM Predicts:** "dog"
*   **Input:** "A quick brown fox jumps over the lazy dog"
*   **LLM Predicts:** "STOPS" (End of sentence)

This iterative process of predicting the most probable next word allows LLMs to generate coherent and contextually relevant text.

---

## Transformer Architecture: The Foundation of Modern LLMs

Historically, various architectures like Recurrent Neural Networks (RNNs) and Long Short-Term Memory (LSTMs) were used to handle text data. However, the **Transformer architecture**, introduced by Google in 2017 in the paper **Attention Is All You Need**, revolutionized the field of Generative AI. Most modern LLMs, including GPT (Generative Pre-trained Transformer), are built upon this architecture.

### The Memory Fading Problem

Earlier architectures like RNNs and LSTMs processed text sequentially, one word at a time. This led to a significant problem: **memory fading**. In long sentences, the model would often "forget" earlier words by the time it reached the end, making it difficult to understand long-range dependencies.

**Example of Memory Fading:**

```

The movie that my friend told me to watch last week, which had the funny superhero fighting aliens,
it was actually...

```

By the time the model reached "it was actually...", older models struggled to remember what "it" referred to (the movie).

Transformers solve this by looking at the **entire sentence at once**, not word-by-word. This parallel processing allows them to:

*   Understand relationships in long sentences (e.g., "movie" connects to "amazing").
*   Retain information from earlier words.
*   Train and generate much faster.

---


## Pre-processing Steps: Preparing Text for the LLM

LLMs don't directly understand text, they operate on numbers. Therefore, input text must be converted into a numerical format through a series of pre-processing steps:

1.  **Tokenization**
2.  **Embedding**
3.  **Positional Encoding**

### 1. Tokenization: Breaking Text into Chunks

**Tokenization** is the process of splitting a sentence into smaller parts called **tokens**. Tokens can be:

*   Entire words (e.g., "I", "love", "Tennis")
*   Parts of words (subwords, e.g., "Play" + "ing" for "Playing")
*   Even single characters (e.g., "?")

Think about how you remember a long phone number like "6640230120". Most people break it into smaller, easier-to-remember chunks (e.g., "66 402 301 20"). Similarly, LLMs break text into tokens for easier processing and pattern recognition.

A single word can sometimes be broken into multiple tokens.

**Example:**

*   "I love Tennis." → "I", "love", "Tennis", "."
*   "Playing" → "Play", "ing"

<details>
<summary><strong>Visualizing Tokenization</strong></summary>

You can explore how different models tokenize text using tools like the <a href="https://platform.openai.com/tokenizer" target="_blank">OpenAI Tokenizer</a>. 
</details>
<MultiLineNote>Note that different models use different tokenizers and techniques.
</MultiLineNote>
### 2. Embeddings: Converting Tokens to Numbers

After tokenization, each token is converted into a list of numbers called a **vector**. This numerical representation is known as an **embedding**.

*  Embeddings capture the meaning of a token in a numeric form. They are not random numbers.
*  Embeddings place words in a multi-dimensional space where similar relationships point in the same direction (e.g., the vector difference between "King" and "Queen" might be similar to "Man" and "Woman"). This allows the model to understand relationships between words.

<details>
<summary><strong>Visualizing Embeddings</strong></summary>

Tools like the <a href="https://projector.tensorflow.org/" target="_blank">TensorFlow Projector</a>. can help visualize word embeddings in a 2D or 3D space.
</details>

### 3. Positional Encoding: Adding Order to Parallel Processing

Since Transformers process the entire input simultaneously, it is important to understand the order of words in a sentence. This is where **positional encoding** comes in.

* Positional data is added to each embedding, informing the model about the word's position within the sentence.
* Without positional encodings, a Transformer would consider sentences like "The dog chased the ball" and "The ball chased the dog" to be identical, as it would only see the collection of words, not their sequence.

**Example:**
Input sentences:

*   “The dog chased the ball”
*   “The ball chased the dog”

Both sentences contain the same words, but the order of the words is different, which changes the meaning.Positional encodings, helps the Transformer to understand both the sentences are different.

---

## High-Level Transformer Architecture: Encoder and Decoder in Action

After pre-processing, the numerical representations (embeddings with positional encoding) are fed into the Transformer's core components:

*   **Encoders:** The encoder is responsible for reading and processing these contextual embeddings. It helps in understanding the meaning and the intent behind the input.
*   **Decoders:** The decoder uses the encoder's understanding to decide what token should be generated next, producing the output sequentially.

This encoder-decoder flow is what allows LLMs to both understand and generate language effectively.