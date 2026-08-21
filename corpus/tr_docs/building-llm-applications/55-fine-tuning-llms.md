# Fine-Tuning LLMs

**Course:** Building LLM Applications  
**Topic:** Running Models locally and Fine-Tuning LLMs  
**Unit ID:** `a84ba413bb8e4f05a458b059186b3c04` | **Unit Number:** 55

---

# Introduction

In the previous session, we learned how to run models locally using tools like Ollama and LM Studio. In this unit, we will learn about fine-tuning LLMs, explore Full Fine-Tuning and PEFT methods like LoRA and QLoRA, and fine-tune the Gemma model using Unsloth.

---

## Scenario: NDFC Bank Chat

Imagine working as an AI engineer at a bank called NDFC. Customers are asking questions. If we use a plain LLM (like GPT, Llama, etc.) without any specific technique, it gives us a generic answer.

### Challenges

*   It doesn't know what kind of credit card the customer has
*   It doesn't know who the customer is
*   No brand-specific tone — just a straight, impersonal answer

### Adding System Prompt (Prompt Engineering)

We add a system prompt: 

```
"Answer in a polite, professional way as an NDFC bank assistant. If you don't know, say you don't know."
```

<b>System Prompt + Question → LLM → Answer</b>

<Section>

**NDFC Bank Chat**
<div style="text-align: right; margin-bottom: 10px;">
        <div style="border: 1px solid #4CAF50; padding: 8px 12px; border-radius: 6px; background-color: #f6fff6; display: inline-block;">
            How much is my credit card late fee?
        </div>
    </div>


<div style="text-align: left;">
        <div style="border: 1px solid #9E9E9E; padding: 8px 12px; border-radius: 6px; background-color: #f5f5f5; display: inline-block;">
            Dear customer, NDFC Bank typically charges a late fee between $30 and $40. For exact details, please check your account statement or contact support.
        </div>
    </div>

</Section>


The tone is polite and professional. But the answer is still vague — it doesn't know the actual late fee amount.

**Prompt Engineering = Formatting and style control.** 

It guides how the model answers, but doesn't give it new knowledge.

### Adding RAG

We connect the LLM to NDFC's private database containing customer account details, transaction histories, and credit card plans. Now the LLM can retrieve specific information.

<Section style="leng: 320px; margin: 40px auto;">

**NDFC Bank Chat**
<div style="text-align: right; margin-bottom: 10px;">
        <div style="border: 1px solid #4CAF50; padding: 8px 12px; border-radius: 6px; background-color: #f6fff6; display: inline-block; max-width: 80%;">
            How much is my credit card late fee?
        </div>
    </div>

<div style="text-align: left;">
        <div style="border: 1px solid #9E9E9E; padding: 8px 12px; border-radius: 6px; background-color: #f5f5f5; display: inline-block; max-width: 80%;">
            Dear customer, According to NDFC Bank's official policy, a late fee of $35 is applied if payment is not made by the due date.
        </div>
    </div>

</Section>

The answer is grounded in actual company data.

**RAG = External knowledge injection.** It connects the model to specific data sources so it can give factual, up-to-date answers.

### Reviewed by Business Manager

"This is good, but we should also suggest: 'You can avoid this by enabling auto-pay.' That's how our best support agents respond."

**Question:**
Where does this suggestion come from? It's not written in any single document. It's a pattern that exists across millions of past chat transcripts — the accumulated knowledge of how NDFC's best agents interact with customers.

We can't just retrieve this from a document. We need the model to learn this behavior from examples.

**Solution: Fine-Tuning**

<b>Fine-Tuning = Domain adaptation and expertise.</b>It changes how the model thinks and behaves.
With fine-tuning, the model learns NDFC's brand voice, its best practices, and its domain expertise

---

##Fine-Tuning
### What is Fine-Tuning?

Fine-tuning is the process of taking a pre-trained language model and further training it on a smaller, specialized dataset to adapt its behavior, style, or knowledge for specific tasks or domains.

It transforms a general-purpose model into a specialized expert using your data, your style, your rules, and task-specific examples.

### Use Cases

**Example 1: College Support Bot**

*   <b>Base Model:</b> Pretrained chatbot (no institution-specific knowledge)
*   <b>Fine-tuning Input:</b> College website, policies, department details, FAQs
*   <b>Result:</b> Bot knows college rules, schedules, admissions, exams, and hostel info

**Example 2: Exam Prep Assistant**

*  <b>Base Model:</b> Summarizer (can summarize any text, not exam-focused)
*  <b>Fine-tuning Input:</b> Syllabus, textbooks, past question papers, model answers, and topper's notes
*  <b>Result:</b> Generates personalized study notes, highlights key topics, answers subject-specific questions

### What Changes During Fine-Tuning?

An LLM is essentially a neural network made up of parameters (weights). During fine-tuning, we update these weights using our specialized dataset. 

### Applications

*   **Domain Adaptation** — Adapting a general pretrained model to a specific domain like medical, legal, or finance
*   **Task Specialization** — Improving performance on a narrow task such as sentiment analysis, question answering, or named entity recognition
*   **Language/Style Customization** — Fine-tuning to handle specific languages, dialects, or writing styles
*   **Personalization** — Customizing a model to reflect user preferences, vocabulary, or tone
*   **Data Efficiency** — Leveraging a small dataset to teach a large model new knowledge instead of training from scratch
*   **Edge Deployment** — Compressing and fine-tuning smaller models for mobile/IoT use cases

---

## Methods Of Fine-Tuning

1.  **Full Fine-Tuning**
2.  **Parameter Efficient Fine-Tuning (PEFT)** — LoRA, QLoRA, and many more

### Full Fine-Tuning

In full fine-tuning, we update all parameters in the entire model. This gives maximum control but requires a lot of compute power and memory.

### Parameter Efficient Fine-Tuning (PEFT)

Instead of updating all parameters, PEFT methods update only a small subset of parameters, making fine-tuning much faster and cheaper.

** PEFT Methods**

- Selective Method 
- Reparameterization (LoRA / QLoRA) 
- Additive Method 
- Soft Prompting 

---

### Full Fine-Tuning vs PEFT

| Aspect | Full Fine-Tuning | PEFT (e.g., LoRA) |
|---|---|---|
| What's updated | All parameters in the entire network | Only small added layers/matrices |
| Cost | Very expensive | Much cheaper |
| Hardware needed | Multiple high-end GPUs | Single consumer GPU possible |
| Risk | Can "forget" general knowledge (catastrophic forgetting) | Preserves base model knowledge |
| When to use | Need maximum domain adaptation | Need efficient, targeted adaptation |

---

## When to Use What?

| Need | Solution |
|---|---|
| Better formatting, tone, or style | Prompt Engineering |
| Access to specific/private/up-to-date documents | RAG |
| Consistent behavior, domain expertise, or learned patterns | Fine-Tuning |
| All of the above | Combine All Three (This is what production systems do!) |

---

## Fine-Tuning a Large Language Model

### What We're Building

**Goal:** Take a base LLM and fine-tune it to respond like a Martian alien — with broken grammar, unique slang, and a consistent alien personality.

**Before Fine-Tuning**

(base model response to "Hello there"):

> "Hello! How can I help you today?"

**After Fine-Tuning** (what we want):

> "Gree-tongz, Terran. You'z a long way from da Blue-Sphere, yez?"

### The Process

1.  Select Base Model
2.  Choose Fine-Tuning Method
3.  Prepare Dataset
4.  Train
5.  Evaluate and Iterate

### Frameworks for Fine-Tuning

Just like we used LangChain as a framework for building agents, we need frameworks for fine-tuning:

*   **Unsloth**
*   **Hugging Face**
*   **Axolotl**
*   **DeepSpeed**
*   **LLaMA Factory**

---

## Steps to Fine-Tune

1.  Install Dependencies and Load Base Model
2.  Test Model Before Fine-Tuning
3.  Apply PEFT (Configure LoRA)
4.  Load and Prepare Dataset
5.  Train and Test the Fine-Tuned Model

## Using Unsloth

Unsloth makes LLM fine-tuning fast and memory-efficient, even on limited hardware.

**Features:**

*   2-5x Faster training
*   70-80% less memory
*   0% Accuracy loss
*   Works on Colab (Free tier)
*   Supports popular models

## Step 1: Install Dependencies and Load Base Model

### Colab Notebook

Open the Google Colab provided below the session. Google Colab provides free Tesla T4 GPU — enough for our fine-tuning.

<MultiLineNote> Need to change resource type to T4 GPU.
</MultiLineNote>
### Install Dependencies

```python
%%capture
!pip install --upgrade --no-cache-dir unsloth unsloth_zoo
!pip install --upgrade --no-deps trl peft accelerate bitsandbytes xformers
```

### Which Models Can We Fine-Tune?

*   Gemma 3 (270M, 1B, 4B, 12B, 27B)
*   Llama 3.2, Llama 3.1, Llama 3
*   Mistral 7B, Mistral
*   Phi-3, Phi-4
*   Qwen 2.5
*   GPT-3.5, GPT-4 (via API only)

**We Choose Gemma 3 270M** — Open-source model by Google, designed for fine-tuning on limited hardware.

### Load the Model Using Unsloth

Unsloth provides a method called `FastModel.from_pretrained()` that loads a model and makes it ready for fine-tuning. It also handles setting up the model efficiently to save memory.

```python
from unsloth import FastModel

model, tokenizer = FastModel.from_pretrained(
    model_name = "unsloth/gemma-3-270m-it",
    max_seq_length = 2048,
    load_in_4bit = True,
    load_in_8bit = False,
    full_finetuning = False,
)
```

*   `model` — Loaded Gemma model for fine-tuning
*   `tokenizer` — Converts text ↔ tokens (words/subwords) for the model
*   `max_seq_length = 2048` — The model can read up to 2048 tokens at once
*   `load_in_4bit = True` — Compress the model to use less memory (called quantization — like compressing an image to save space, but for model weights)
*   `load_in_8bit = False` — 8-bit compression is not used
*   `full_finetuning = False` — Tells Unsloth that we don't want to use full fine-tune

## Step 2: Test Model Before Fine-Tuning

Before fine-tuning, let's see how the base model responds. This gives us a baseline to compare against later.

### Understanding Chat Template

Every model has its own chat format with special tokens. `tokenizer.apply_chat_template()` converts our message into the format the model expects.

**Applying Chat Template**

For Gemma 3, the chat template looks like this:

```
<bos><start_of_turn>user
Hello there.<end_of_turn>
<start_of_turn>model...
...
<eos>
```

*   `<bos>` — Beginning of Sequence
*   `<start_of_turn>` — Marks where a message starts
*   `<end_of_turn>` — Marks where a message ends
*   `<eos>` — End of Sequence

### Inference Function

We define a helper function that takes a message, sends it to the model, and prints the response. 

- The `model.generate()` method is what actually produces the model's output.
- `apply_chat_template` This converts our message into the format Model expects


```python
from transformers import TextStreamer

def do_inference(messages, max_new_tokens=128):
    _ = model.generate(
        **tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        ).to("cuda"),
        max_new_tokens=max_new_tokens,
        temperature=1.0,
        top_p=0.95,
        top_k=64,
        streamer=TextStreamer(tokenizer, skip_prompt=True),
    )
```

*   `.to("cuda")` — Sends the data to the GPU for fast processing
*   `streamer` — Prints each word as it's generated

<MultiLineNote> The remaining parameters like temperature, top_p, top_k control how the model generates text. We'll understand these in detail in further sessions.
</MultiLineNote> 

### Testing the Model

```python
messages = [{"role": "user", "content": "Hello there."}]
do_inference(messages)
```

**Expected Output:** "Hello! How can I help you today?"

The model responds in normal, polished English.

## Step 3: Apply PEFT (Configure LoRA)

Now we need to tell the model which parts to make trainable. We're going with PEFT. Specifically, we'll use LoRA (Low-Rank Adaptation) — the most popular PEFT method.

### How LoRA Works

1.  Freeze all the original model weights (keep them unchanged)
2.  Add small trainable matrices (called adapters) alongside the frozen weights
3.  Train only these small adapter matrices

### Using QLoRA

Since we loaded our model with `load_in_4bit = True`, we're actually using QLoRA (Quantized LoRA) — the model is compressed to 4-bit and then LoRA adapters are applied on top. This means even less memory usage.

### Configure LoRA Using Unsloth

Unsloth provides `FastModel.get_peft_model()` to set up LoRA. This method takes our model and adds small trainable adapters to it.

```python
model = FastModel.get_peft_model(
    model,
    finetune_vision_layers = False,
    finetune_language_layers = True,
    finetune_attention_modules = True,
    finetune_mlp_modules = True,
    r = 8,
    lora_alpha = 8,
    lora_dropout = 0,
    bias = "none",
    random_state = 3407,
    use_gradient_checkpointing = "unsloth",
)
```

*   `finetune_vision_layers = False` — We are not training image layers (text only)
*   `finetune_language_layers = True` — We train text-related layers
*   `finetune_attention_modules = True` — Train attention heads (how the model focuses on input)
*   `finetune_mlp_modules = True` — Train reasoning layers (Multi Layer Perceptron / Feed Forward Network)
*   `r = 8` — Rank of adapters

<MultiLineNote>We'll understand the remaining parameters in detail in further sessions. </MultiLineNote>
 

## Step 4: Load and Prepare Dataset

### Dataset Selection & Fine-tuning Options

*   Search for datasets for your use case  — personal documents, domain-specific (Healthcare, Law, Finance, E-commerce, Education), or public datasets (Kaggle, Hugging Face, etc.)
*   Adapt relevant dataset — adapt datasets based on your specific use case
*   Prepare (transform/clean, if needed) — some datasets are freely available; others require manual preparation

### Martian NPC Dataset

The `bebechien/MobileGameNPC` dataset provides sample conversations between a player and an alien NPC (a Martian) with a unique speaking style.

The Martian NPC's speaking style:

*   Replaces 's' sounds with 'z' ("is" → "iz")
*   Uses 'da' for 'the'
*   Uses 'diz' for 'this'
*   Includes occasional clicks like *k'tak*
*   Has a consistent alien personality

Sample data: <a href="https://huggingface.co/datasets/bebechien/MobileGameNPC/viewer/martian/train" target="_blank>Huggingface</a>This dataset has only 25 examples — for teaching a consistent speaking style, even a small, high-quality dataset works.

### Load the Dataset

```python
from datasets import load_dataset

dataset = load_dataset("bebechien/MobileGameNPC", "martian", split="train")
```

*   `"bebechien/MobileGameNPC"` — Dataset name
*   `"martian"` — Specific subset/configuration (Martian NPC conversations)
*   `split="train"` — Loads only the training part of the dataset

### What is Split?

Datasets are usually divided into parts:

*   **train** — Used to train the model
*   **validation** — Used to check performance during training
*   **test** — Used to evaluate final performance

### Inspecting the Data

```python
print(f"Total samples: {len(dataset)}")
print(f"Columns: {dataset.column_names}")
print(f"player: {dataset[0]['player']}")
print(f"alien:  {dataset[0]['alien']}")
```

### Format for Training

Every model has a specific chat template — a format with special tokens that the model was trained to understand. If we don't follow this format, the model won't learn properly.

**Gemma 3 Chat Template**

```
<bos><start_of_turn>user
Hello there.<end_of_turn>
<start_of_turn>model Gree-tongz, Terran. 
You’z a long way from da Blue-Sphere, yez?<end_of_turn>...<eos>
```


** Loading Gemma 3's Chat Template**


```python
from unsloth.chat_templates import get_chat_template

tokenizer = get_chat_template(tokenizer, chat_template="gemma-3")
```

This tells the tokenizer to use Gemma 3's special tokens (`<start_of_turn>`, `<end_of_turn>`, etc.) when formatting conversations.

** Converting Player Pairs to Chat Format**

Our dataset has `player` and `alien` columns. We need to convert them into the chat format.

```python
formatted_texts = []
for i in range(len(dataset)):
    conversation = [
        {"role": "user", "content": dataset[i]["player"]},
        {"role": "assistant", "content": dataset[i]["alien"]},
    ]
    text = tokenizer.apply_chat_template(
        conversation,
        tokenize=False,
        add_generation_prompt=False
    )
    formatted_texts.append(text)
dataset = dataset.add_column("text", formatted_texts)
```

*   For each row, we create a conversation with user (player) and assistant (alien) roles
*   `apply_chat_template` wraps it in Gemma's special tokens format
*   We add the formatted text as a new "text" column to our dataset

**Verify the Conversion**

```python
print("--- After conversion (what model will train on) ---")
print(dataset[0]["text"])
```

This should show the text wrapped in Gemma's `<start_of_turn>user ... <end_of_turn>` format.

## Step 5: Train and Test the Fine-Tuned Model

### Training the Model Using SFTTrainer

We use Supervised Fine-Tuning Trainer (SFTTrainer) from the Transformer Reinforcement Learning (trl) library to train the model on our dataset until it learns the Martian speaking pattern.

Martian Dataset (Examples) -> SFTTrainer (Fine-Tuning Process) -> Learns Martian Style



```python
from trl import SFTTrainer, SFTConfig
from unsloth import is_bfloat16_supported

trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    args = SFTConfig(
        dataset_text_field = "text",
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 5,
        num_train_epochs = 30,
        learning_rate = 2e-4,
        fp16 = not is_bfloat16_supported(),
        bf16 = is_bfloat16_supported(),
        logging_steps = 5,
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
        report_to = "none",
    ),
)
trainer.train()
```

*   `dataset_text_field = "text"` — Which column to use from dataset
*   `num_train_epochs = 30` — Number of passes of the entire dataset through the model
*   `learning_rate = 2e-4` — Controls by how much the weights are changed based on the error
*   ` fp16 = not is_bfloat16_supported(), bf16 = is_bfloat16_supported(),` — BFloat16 offers larger range but lower precision than the FloatingPoint16 (when storing weights)
      
<MultiLineNote> The training parameters like learning_rate, gradient_accumulation_steps, warmup_steps, etc. control how the model learns. We'll understand all of these in detail in further sessions.
</MultiLineNote>


### Test After Fine-Tuning

Now the moment of truth! Let's test the fine-tuned model with the same input we used for our baseline:

```python
model = FastModel.for_inference(model)
do_inference([{"role": "user", "content": "Hello there."}])
```

**Expected Output:** "Gree-tongz, Terran. You'z a long way from da Blue-Sphere, yez?"

Compare this with the baseline — the model has completely transformed its personality!

---

#### Here is the <a href="https://colab.research.google.com/drive/1oxvplqO6XdvUwuKmVHSRLsJMoXPJ4kVO#scrollTo=LAiv-wiacKOO" target="_blank" rel="noopener noreferrer">Fine-tuning LLMs Final Code (Google Colab)</a>

---

## Try It Yourself

1.  **Fine-tune Stable Diffusion** — Customize image generation for your style, domain, or use case (product photography, art styles, etc.)
2.  **Fine-tune a TTS Model** — Adapt text-to-speech models to generate speech in your own voice with different emotions and tones
3.  **Pick Any Dataset** — Select a dataset from any domain (customer support, medical records, legal documents) and experiment with fine-tuning
4.  **Experiment with Different Models** — Try various base (foundation) models (Llama, Gemma, Mistral) with different datasets and compare results to find the best fit for your use case