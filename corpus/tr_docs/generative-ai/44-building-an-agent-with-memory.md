# Building an Agent with Memory

**Course:** Generative AI  
**Topic:** Agents with Memory & Introduction to MCP  
**Unit ID:** `c1540365c966474581da649d925824fd` | **Unit Number:** 44

---

# Building an Agent with Memory

In this session, we will explore agents with memory and Adding Memory to AI Shopping Assistant

## What is an AI Agent?

An AI agent is a system that works autonomously to achieve a specific goal. The core components of an agent are:

-   **AI Model:** The "brain" of the agent (e.g., GPT-4, Claude).
-   **Tools:** External resources the agent can use (e.g., search engines, databases).
-   **Memory:** The agent's ability to store and recall information.

This session will focus on the **memory** component.

## Agents with Memory

Agents with memory are AI systems that can store and use past information to make better, more context-aware decisions. They combine a large language model with a persistent memory store.

### Why is Memory Important?

Memory allows an agent to:

-   **Store information:** Keep a record of important details from previous interactions.
-   **Learn from past interactions:** Refine its responses based on what it has "learned."
-   **Maintain context and continuity:** Turn isolated conversations into a single, continuous dialogue.

Without memory, an agent treats every interaction as a new one, unable to recall previous instructions, preferences, or context.

### Example: Agent without Memory

Imagine you tell a shopping assistant that you're a vegetarian. The next day, you ask for dinner suggestions, and it recommends grilled chicken. This is because the agent has no memory of your dietary preference.

### Example: Agent with Memory

A customer support chatbot with memory can recall your previous complaints and the steps already taken to resolve an issue. This saves you from repeating information and leads to a much better experience.

## Types of Memory in AI Agents

There are two main types of memory used in AI agents:

1.  **Short-Term Memory**
2.  **Long-Term Memory**

### Short-Term Memory

Short-term memory is the agent's ability to remember information relevant to the **current conversation or session**. This includes:

-   Recent messages
-   Results from tool calls
-   Current task context

#### Context Window

Short-term memory is limited by the model's **context window**. The context window is the maximum amount of text the model can process at once to generate a response. If a conversation exceeds the context window, the model may "forget" earlier parts of the conversation.

#### Implementing Short-Term Memory in n8n

n8n provides a **Simple Memory** node that stores a chat history for the current session. This gives your agent context across interactions within that session. You can configure it with a unique session key (like a Telegram chat ID) to keep conversations separate for each user.

### Long-Term Memory

Long-term memory allows an agent to retain information **across multiple sessions and interactions**. This is crucial for personalization and learning over time. This includes:

-   User preferences
-   Historical interaction data
-   Learned behaviors

#### Implementing Long-Term Memory

Long-term memory can be implemented using external data stores like:

-   **Databases:** Airtable, Google Sheets
-   **Vector Databases:** Pinecone

#### Types of Long-Term Memory

Long-term memory can be further categorized into:

-   **Episodic Memory:** Stores specific events and experiences .
-   **Procedural Memory:** Stores learned skills and "how-to" knowledge .
-   **Semantic Memory:** Stores general knowledge, facts, and concepts .

## Building an AI Shopping Assistant with Memory

Now, let's apply these concepts to a practical example. We will build an AI shopping assistant that:

-   Uses session-based memory to understand your style and product needs during a conversation.
-   Stores your conversation history and preferences for personalized suggestions.

This will allow the agent to provide a more adaptive and context-aware experience, making it a much more helpful assistant.

### Adding Memory to the AI Shopping Assistant

To add memory to our AI Shopping Assistant, we will use the **Simple Memory** node in n8n. Here's how to configure it:

1.  **Add the Simple Memory Node:** Add a `Simple Memory` node to your workflow.
2.  **Connect it to the AI Agent:** Connect the `Simple Memory` node to the `Memory` input of the `AI Agent` node.
3.  **Configure the Session Key:**
    *   Set the **Session Key** to a unique identifier for each user. For a Telegram bot, you can use the chat ID (`{{ $json.message.chat.id }}`). This ensures that the agent maintains a separate memory for each user.
4.  **Set the Context Window Length:**
    *   You can define how many recent messages the assistant remembers during the conversation. A good starting point is 10.

By adding this memory node, our shopping assistant will now be able to remember the context of the conversation, leading to more personalized and relevant recommendations.