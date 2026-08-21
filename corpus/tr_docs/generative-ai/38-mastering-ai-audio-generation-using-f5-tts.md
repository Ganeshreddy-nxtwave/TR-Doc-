# Mastering AI Audio Generation using F5-TTS

**Course:** Generative AI  
**Topic:** Mastering Audio Generation & No-Code Application Building  
**Unit ID:** `df19782df8754576b84e90950d9ae9b0` | **Unit Number:** 38

---

# Introduction

In the previous unit we understand the core concepts of text-to-speech, speech-to-text, and speech-to-speech technologies and built a podcast generator. In this unit, we'll go beyond the basics and explore how to add emotion and nuance to our AI-generated audio using F5-TTS.


## Mastering AI Audio Generation using F5-TTS | Part 2


### What We’ve Explored So Far

We have looked at various closed and open-source audio generation models, including online platforms like ElevenLabs and Murf AI.

### Challenges with Third-Party Providers

While convenient, these services come with challenges:

- **Costs**: Subscription fees can add up.
- **Limited Customization**: You have less control over the final output.
- **Daily Limits**: Many services restrict the amount of audio you can generate.
- **No Full Control**: You are dependent on the provider's infrastructure.
- **Privacy Concerns**: Your data is processed on external servers.

What if the same powerful AI audio generation model could run on your own machine, without external providers? This is where open-source models come in.

### Open Source Audio Generation Models

- F5-TTS
- MeloTTS
- Whisper
- OpenVoice V2
- …and many more

## Introducing F5-TTS

F5-TTS is an AI-powered text-to-speech synthesis tool that converts text into natural-sounding speech. It offers real-time processing, making it ideal for creating dynamic audio content, voice-overs, and digital narratives.

### Why F5-TTS?

- **Open-source**: Free to use and modify.
- **Voice Cloning**: Clone any voice with just a short audio sample.
- **Natural Speech**: Creates human-like speech.
- **Free**: Completely free to use.

### Features of F5-TTS

1.  **Zero-shot voice cloning**
2.  **Multi-language and emotional control support**
3.  **Unlimited voice generation**
4.  **Keep creations private & secure**
5.  **Understand the real technology behind it**

---

## Let's Run the F5-TTS Model Ourselves!

<details>
<summary><strong>Prerequisites</strong></summary><br>

Running an audio generation model requires a GPU. However, free cloud GPU access is available through platforms like Kaggle.

<a href="https://learning.ccbp.in/course?c_id=b9811b34-585b-47e0-a0be-65f1081a74f2&s_id=04b5d8ae-3e91-4215-be28-63ec61554c26&t_id=4915a7b0-b8d7-4148-8914-d8d3fb086944" target="_blank">Kaggle Setup</a>
</details>

<details>
<summary><strong>Connect to F5-TTS Interface</strong></summary><br>

After the Kaggle setup, executes notebook successfully, it will generate URLs that connect directly to the F5-TTS interface.

<a href="https://www.kaggle.com/code/contentgenai/mastering-ai-audio-generation-using-f5-tts" target="_blank">Master Audio Generation using F5-TTS Notebook</a>
</details>

<MultiLineNote>
**CHECK BEFORE PROCEEDING**: Make sure your Kaggle notebook is ready and running with GPU enabled.
</MultiLineNote>

---

## Creating a Podcast with F5-TTS

The process is straightforward:
**Write your script >> Input it into F5-TTS >> Get professional narration instantly**

### Steps to be Followed

<details>
<summary><strong>Step 1: Upload a Voice Sample</strong></summary><br>

#### Basic TTS: Uploading Audio Reference

- **How to use?**: Upload a voice sample (3-10 seconds) or record directly using the mic icon.
- **Why it matters?**: The model learns the voice characteristics, capturing tone, pitch, and accent.
- **Tip**: Use clear speech with minimal background noise.
- <a href="https://nkb-backend-ccbp-media-static.s3-ap-south-1.amazonaws.com/ccbp_beta/media/content_loading/uploads/36d060ec-f8b6-401a-a8e1-c9b9a6db5450_example.mp3" > Sample Audio File </a>
- Reference Text

```
Generative AI creates new content, like text or images, based on patterns in data. Large Language Models (LLMs) are a powerful form of this AI, generating human-like text, while Small Language Models (SLMs) focus on specialized tasks with less data. 
```

</details>

<details>
<summary><strong>Step 2: Enter the Text from Your Voice Sample</strong></summary><br>

#### Basic TTS: Reference Text

- **What to enter?**: The exact text spoken in the reference audio you uploaded.
- **Why it matters?**: If provided, the model aligns speech patterns correctly. If left blank, it auto-transcribes using the Whisper model, which might be less accurate.
- **Tip**: Always provide the text if possible for the best results.
</details>

<details>
<summary><strong>Step 3: Input Your Podcast Script</strong></summary><br>

#### Basic TTS: Text To Generate

- **What is it?**: The new text that you want the AI to generate in the cloned voice.
- **Use Cases**: Convert podcast scripts to audio, generate audio for videos, etc.

#### Example Podcast Script:

```
Generative AI, sometimes called gen AI, is artificial intelligence (AI) that can create original content such as text, images, video, audio or software code in response to a user’s prompt or request.

Generative AI relies on sophisticated machine learning models called deep learning models algorithms that simulate the learning and decision-making processes of the human brain. These models work by identifying and encoding the patterns and relationships in huge amounts of data, and then using that information to understand users' natural language requests or questions and respond with relevant new content.

AI has been a hot technology topic for the past decade, but generative AI, and specifically the arrival of ChatGPT in 2022, has thrust AI into worldwide headlines and launched an unprecedented surge of AI innovation and adoption. Generative AI offers enormous productivity benefits for individuals and organizations, and while it also presents very real challenges and risks, businesses are forging ahead, exploring how the technology can improve their internal workflows and enrich their products and services. According to research by the management consulting firm McKinsey, one third of organizations are already using generative AI regularly in at least one business function.¹ Industry analyst Gartner projects more than 80% of organizations will have deployed generative AI applications or used generative AI application programming interfaces (APIs) by 2026
```
</details>

<details>
<summary><strong>Step 4: Generate Podcast</strong></summary><br>

Click the generate button, and F5-TTS will produce the audio output. You will have a professional podcast narration ready to download.
</details>

---

## Enhancing the Podcast by Adding Emotions with F5-TTS

### Steps to be Followed

<details>
<summary><strong>Step 1: Upload Multiple Voice Samples with Different Emotions</strong></summary><br>

#### Multi Speech: Reference Audio

Upload multiple audio clips, each with a specific speech type name (e.g., "neutral", "sad", "anger", "surprise"). Each clip should represent a different voice, accent, or emotional style.

- <a href="https://nkb-backend-ccbp-media-static.s3-ap-south-1.amazonaws.com/ccbp_beta/media/content_loading/uploads/d9abe905-b7e6-4052-94d9-77bd8fe13939_neutral016%20(1).wav" > Neutral Audio File </a>
- <a href="https://nkb-backend-ccbp-media-static.s3-ap-south-1.amazonaws.com/ccbp_beta/media/content_loading/uploads/768692de-1184-4174-b119-ce88377c681b_sad016%20(1).wav" > Sad Audio File </a>
- <a href="https://nkb-backend-ccbp-media-static.s3-ap-south-1.amazonaws.com/ccbp_beta/media/content_loading/uploads/fa6d5d90-6027-4eca-9aa4-11f8af3cb87b_anger016%20(1).wav" > Anger Audio File </a>
- <a href="https://nkb-backend-ccbp-media-static.s3-ap-south-1.amazonaws.com/ccbp_beta/media/content_loading/uploads/4c0d885e-9088-4a7d-9b89-9d4489546c4a_surprise016%20(1).wav" > Surprise Audio File </a>

</details>

<details>
<summary><strong>Step 2: Enter the Text Spoken in each Voice Sample</strong></summary><br>

#### Multi Speech: Reference Text

Each reference audio needs its exact transcription for accurate speech alignment. If left blank, the system auto-transcribes, but with lower accuracy.
</details>

<details>
<summary><strong>Step 3: Format Script with Emotion Tags</strong></summary><br>

#### Multi Speech: Text to Generate

Enter your script with the speech type names at the beginning of each block to tell the model which emotion to use. This allows you to combine multiple styles in one input, and the model will switch tone/voice accordingly.

#### Example Script with Emotion Tags:

```
{neutral} Generative AI, sometimes called gen AI, is artificial intelligence (AI) that can create original content such as text, images, video, audio, or software code in response to a user’s prompt or request.

{sad} Generative AI relies on sophisticated machine learning models called deep learning algorithms that simulate the learning and decision-making processes of the human brain. These models work by identifying and encoding the patterns and relationships in huge amounts of data, and then using that information to understand users' natural language requests or questions and respond with relevant new content.

{anger} AI has been a hot technology topic for the past decade, but generative AI, and specifically the arrival of ChatGPT in 2022, has thrust AI into worldwide headlines and launched an unprecedented surge of AI innovation and adoption.

{surprise} Generative AI offers enormous productivity benefits for individuals and organizations. While it also presents real challenges and risks, businesses are forging ahead, exploring how the technology can improve workflows and enrich products and services. According to research by McKinsey, one-third of organizations are already using generative AI regularly in at least one business function. Industry analyst Gartner projects that more than 80% of organizations will have deployed generative AI applications or APIs by 2026!
```
</details>

<details>
<summary><strong>Step 4: Generate Enhanced Podcast</strong></summary><br>

After formatting your script with emotion tags, click generate. The output will be an enhanced podcast audio with multiple emotions.
</details>

---

## Voice-Chat

F5-TTS also includes a Voice-Chat feature. You can have a conversation with an AI using your reference voice!

- Upload an audio clip and optionally text.
- Load the chat model.
- Record your message through your microphone or type it.
- The AI will respond using the reference voice.