# Build Your Own AI Shopping Assistant | Part 2

**Course:** Generative AI  
**Topic:** Building an AI Shopping Assistant  
**Unit ID:** `ce49c8722e3f4757873b0bfd0b9a56fe` | **Unit Number:** 42

---

In the previous part, we learned how to build an AI-powered shopping assistant on Telegram. In this section, we will enhance the assistant by adding **voice input** functionality. This will allow users to speak their product requests instead of typing them, making the shopping experience more intuitive and accessible.

> _"Have you ever found it difficult to type your shopping queries? Let’s explore how voice input can improve the shopping assistant experience."_

> _"In this section, we will guide you through the steps of adding voice message support to the AI shopping assistant, enabling automatic speech-to-text conversion for better interaction."_

## 1. Enhancing the Telegram Shopping Assistant with Audio Support

While AI models can understand and respond to text, they cannot directly process audio. To address this challenge, we need to convert **audio messages** into **text** before passing them to the AI model for processing.

- **Get Audio File**: The first step is to download the audio message.
- **Transcribe Audio to Text**: Use a speech-to-text model to convert audio to text.
- **Merge Audio and Text Paths**: Both text and audio queries should lead to the same AI agent for processing.

**Steps to Implement Audio Support:**

1. Adding Message Type Check
2. Get Audio File
3. Transcribing Audio to Text
4. Merging Audio and Text Paths

### 1.1 Adding Message Type Check

Since messages arrive in two formats—text and audio—we need to route each type correctly:

- **Text Messages**: These can be directly sent to the AI agent for processing.
- **Audio Messages**: These need to be converted to text first.

We must distinguish between text and audio messages to process them correctly.

**Steps to Configure Message Type Check**

1. **Add an If Node**: This node will check the message type.

   - If the message is text, it will proceed directly to the AI agent.
   - If the message is audio, it will go through the audio processing steps.

2. **Configure the Condition**:
   - Check if the message is a voice message.
   - If it’s audio, send it for speech-to-text conversion.
   - If it’s text, route it directly to the AI agent.

### 1.2 Downloading Audio File

When a user sends an audio message, Telegram only provides a **File ID**, not the actual audio file. To access the audio, we must use the **Telegram Get File Node**.

** How Does the Telegram Get File Node Work?**

1. The user sends an audio message.
2. Telegram generates a **File ID** for the audio.
3. The **Get File Node** uses the File ID to fetch the actual audio file.
4. Telegram sends the complete audio file, which is then ready for processing.

**Steps to Configure**

1. **Add Telegram Get File Node**: This node is connected to the “true” output of the If node (indicating the message is audio).
2. **Set File ID**: Retrieve the File ID from the incoming audio message and use it to get the full audio file.

The audio file is now available in **.oga** format, which is Telegram’s voice message format.

### 1.3 Transcribing Audio to Text

Once we have the audio file, the next step is to convert it to text so the AI agent can understand and process it.

**Why We Need Transcription**

- **AI models process text, not audio**: To enable the AI to work with audio inputs, we must first convert them to text.

**Using the Whisper API**

We will use the **Whisper API** from OpenAI (hosted by Groq) to transcribe audio to text.

**Groq**: Groq is an AI startup that offers a cloud platform called GroqCloud, where users can access popular models (meta llama, qwen, whisper, etc)

**GroqCloud**: Groq provides a cloud platform that hosts popular AI models, including Whisper, for speech-to-text conversion.

**Steps to Configure**

1. **Use HTTP Request Node**: Make an API call to the Whisper API to transcribe the audio file.
2. **Replace the placeholder** in the API call with the actual Groq API key.
3. **Post the HTTP request** to the Whisper API, which will return the transcribed text.

The Whisper API does not accept **.oga** format, so we must convert the audio to a format that Whisper understands, such as **.ogg**.

**Converting Audio to Supported Format**

Telegram sends voice messages in the **.oga** format, but the Whisper API requires **.ogg**. To resolve this, we need to convert the file format.

We have several options to convert the file:

- Use **n8n nodes** for conversion.
- Use an **external library**.
- Use **Python code** inside the workflow.

**Why Use Python Code?**

Using Python allows us to quickly fix the audio format problem inside our workflow.

**Steps to Configure**

1. **Add Python Code Node**: This node will replace **.oga** with **.ogg** in the file name.
2. **Update File Name**: The Python code will ensure that the file name is correctly formatted before sending it to the Whisper API.

```python
result = _input.first()

if result.binary and 'data' in result.binary:
    if result.binary['data'].get('fileName'):
        updated_filename = result.binary['data']['fileName'].replace('.oga', '.ogg')
        result.binary['data']['fileName'] = updated_filename

return result
```

This code ensures the file name is updated, making it compatible with the Whisper API.

### 1.4 Merging Audio and Text Paths

Now that both text messages and transcribed audio messages can be processed, we need to merge the two paths into a single workflow.

Connecting All Paths

**Text Messages**: Directly route to the AI agent.

**Transcribed Audio**: Route the transcribed text to the AI agent.

Now both types of messages will be processed by the same AI agent, enabling a seamless user experience.

### Final Workflow

1. Message arrives on Telegram.
2. Check message type (text or audio).
3. If text: Directly route to the AI agent.
4. If audio: Convert to text using the Whisper API.
5. Send the processed text to the AI agent.
6. The AI agent finds relevant products and sends the response back to the user on Telegram.

You now have a fully functional AI Shopping Assistant on Telegram that supports both text and voice input.