# Understanding How LLMs Work | Part 2

**Course:** Building LLM Applications  
**Topic:** Understanding How LLMs Works & Enhancing Productivity with AI  
**Unit ID:** `bff02648761147f6baeacb6ecf2a1f86` | **Unit Number:** 15

---

# Understanding How LLMs Work | Part 2

## Introduction

In Part 1, we explored the foundational concepts of Large Language Models (LLMs), including their core function of next-word prediction, the necessity of the Transformer architecture, and the initial pre-processing steps (Tokenization, Embedding, and Positional Encoding). Now lets understand the internal workings of the Transformer's Encoder and Decoder components.

---

## Transformer Architecture: The Encoder

As discussed, the **Encoder** is responsible for reading and processing the input embeddings to understand the meaning and intent behind the text. Each encoder layer consists of several sub-layers:

1.  **Multi-Head Attention**
2.  **Add & Norm **
3.  **Feed-Forward Network**

### 1. Multi-Head Attention

Multi-Head Attention is crucial for capturing diverse relationships (syntactic, semantic, emotional) within the input sentence. It achieves this through multiple "heads," each focusing on a slightly different aspect of the relationships between words.

*   **Self-Attention:** The core mechanism within Multi-Head Attention is **Self-Attention**. For each word in a sentence, Self-Attention computes how much focus that word should give to every other word in the same sentence to understand its context.

    **Example:** In "She saw a bat."
    *   If the surrounding text is about cricket, "bat" will be strongly associated with a cricket bat.
    *   If the text is about nocturnal animals, "bat" will be strongly associated with the animal.

    This mechanism allows the model to capture complex relationships and disambiguate word meanings based on context.

### 2. Add & Norm

This sub-layer performs two critical functions:

*   **Add :** Adding outputs from multiple heads along with input to preserve 
original information. 
*   **Norm(Noramalizaton) :** Maintains the numbers within working range of [-1, 1]. 
Sets mean = 0 and standard deviation = 1

### 3. Feed-Forward Network (FFN)

* Further mix and transform the processed information from the attention layer.
* Expand the representation to capture richer and better features. 

    ** Example:** 
    
    - The word "bat" might be expanded into features like "cricket, game, sport" or "mammal, wings, night" depending on the context.

These layers are typically stacked multiple times to create a encoder. The final output of the encoder is a set of **contextual embeddings**, which represent each token's meaning shaped by its surrounding tokens.

---

## Transformer Architecture: The Decoder

The **Decoder** is responsible for generating the output sequence, one token at a time, based on the encoder's understanding and the previously generated tokens. Each decoder layer also has several sub-layers:

1.  **Masked Multi-Head Attention (Self-Attention)**
2.  **Multi-Head Attention (Cross-Attention)**
3.  **Add & Norm**
4.  **Feed-Forward Network (FFN)**

### 1. Masked Multi-Head Attention (Self-Attention)

This is similar to the encoder's Multi-Head Attention but with a crucial difference: **masking**.

During training, the decoder is prevented from "looking ahead" at future tokens in the target sequence. It can only attend to the words that have already been generated.

### 2. Multi-Head Attention (Cross-Attention)

This attention mechanism allows the decoder to focus on relevant parts of the **encoder's output** (the contextual embeddings). It asks, "What's most important from the input right now?" and gets fresh answers from the encoder for each token it generates.


### 3. Feed Forward Neural Network and Add & Norm

These layers function similarly to their counterparts in the encoder, transforming and normalizing the information to produce richer features and prevent context loss. However, the specific transformations learned will be different due to their role in generation rather than just understanding.

---

## How LLMs Work: Flow Overview

In summary, the process of an LLM generating a response involves four main steps:

1.  **Input Processing:** The input text is tokenized, embedded, and positional encodings are added.
2.  **Encoder Captures Context:** The encoder processes these numerical inputs, using Multi-Head Attention, Add & Norm, and FFNs to build a rich contextual understanding.
3.  **Decoder Generates Output:** The decoder uses Masked Multi-Head Attention (for self-attention), Cross-Attention (to interact with the encoder's output), Add & Norm, and FFNs to generate output embeddings sequentially.
4.  **Converting Output to Natural Language:** The Linear and Softmax layers convert the decoder's output embeddings into actual words, predicting the most probable next token until the response is complete.

---

## Future Trends in LLMs

The field of LLMs is rapidly evolving, with key trends including:

*   **Larger Contexts:** Continued expansion to multi-million token windows for processing entire books, videos, and vast datasets.
*   **Enhanced Reasoning:** Development of models that prioritize step-by-step thinking and more robust logical capabilities.
*   **Multimodality:** Seamless integration of various data types like text, images, audio, and video (e.g., Google Gemini).
*   **Ethics:** Ongoing focus on developing better safeguards against biases, hallucinations, and other ethical concerns.

Staying updated with these advancements is essential as LLMs continue to reshape technology and applications.