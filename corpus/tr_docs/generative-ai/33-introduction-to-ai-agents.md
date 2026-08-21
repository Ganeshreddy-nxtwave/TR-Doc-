# Introduction to AI Agents

**Course:** Generative AI  
**Topic:** Building AI Agents  
**Unit ID:** `2e566865957343ed9579b659d494dc63` | **Unit Number:** 33

---

# Introduction to AI Agents

In the previous units, we learned about AI tools like ChatGPT Agents and we learned about building automated workflows using n8n and integrating AI for tasks like content creation and summarization. In this unit, we'll explore AI Agents — intelligent systems that can think, plan, and take actions autonomously to achieve specific goals.

## Introduction to AI Agents

- An AI agent is a system that can operate independently to achieve a specific goal without constant human intervention

AI Agents can:

1. **Understand** what you want
2. **Reason** and plan how to accomplish the task
3. **Execute** actions on our behalf
4. Learn from **success** and **failures**

###Understanding with Analogy

Let’s understand with a babysitter analogy

- When parents leave a child with a babysitter, they provide:
    - Basic instructions (bedtime, emergency contacts)
    - Resources (food, phone numbers)
    - The overall mission (keep the child safe and happy)
- They don’t micromanage; the babysitter uses judgment to handle situations.”

### Why Agents Are Needed

- To solve complex tasks
- Learn user preferences and tailor approach
- Need for autonomy

---

##Core Components

- AI Model (like GPT-5 or Claude)
- Tools (search engines, databases)
- Memory

###AI Model - LLM

- The model is essentially the agent’s “brain” – it interprets instructions, reasons about problems, and decides on actions (GPT-5, Claude, Llama, etc)
- The "brain" of the agent that can do
    - Goal Understanding
    - Planning & Reasoning
    - Adaptive Learning
    - Learning

###Tools

- Tools are external functions or interfaces the agent can use to interact with the outside world
- Tools are the agent's "arms and legs".
    - Extends Capabilities: Allow the agent to perform actions it couldn't do alone
    - Access Real-Time Data: Connect to current information beyond the model's training cutoff
    - Executes Specific Functions: Perform specialized tasks with precision

**Commonly Used Tools**
 
- **Web Search**       Allows the agent to fetch up-to-date information from the internet 
- **Image Generation** Creates images based on text descriptions 
- **Retrieval**        Retrieves information from an external source 
- **API Interface**    Interacts with an external API (GitHub, YouTube, Spotify, SERP API etc.) 

###Memory

- Memory allows the agent to
    - Store information
    - Learn from past interactions
    - Maintain context and  continuity

---

##How Agents Work

- Agents operate in a continuous loop that integrates the components
- Some of the commonly used Frameworks are:
    - ReAct
    - Tool Use
    - Reflection

###ReAct - Reasoning and Acting

One of the most commonly used patterns is:

- Thought / Reason
- Action
- Observation

**Thought**

- The agent receives information
- Understands the information
- Reasons and decides the next steps based on the observation

**Action**

- The agent identifies a specific action
- Uses an appropriate tool to perform that action

**Observation**

- Agent evaluates the outcome of its action
- Compares it with expected results
- Refines understanding and approach based on feedback

###Common Pattern - ReAct

- The ReAct pattern involves three main stages — *Thought, Action,* and *Observation* — which repeat in a loop.  
- This allows the agent to reason through problems, perform actions, observe outcomes, and refine its approach until it reaches the final **Answer**.

###Example

- Let’s say you have to book a travel vacation to Ooty

**Planning Travel Vacation - Human  **

- Opening Booking App
- Searching for flights
- Searching for Hotels
- Choosing Best Options
- Booking Flight

**Booking a Travel Vacation**

Think of an AI agent as a smart helper that can work on its own to get things done

- ` Define Goal`: 
    Set the objective for the AI agent
- `Execute Task`: Autonomously performs necessary actions 
- `Complete Booking`: Vacation bookings are successfully finalized 

**Example: **

`Plan a vacation to Ooty for three people with a budget of 20,000 INR`

<details>
<summary><b>Loop 1: Initial Assessment</b></summary>

#### Thought
I need to plan a vacation to Ooty for three people with a focus on budget, food, and activities.

#### Action
Search for **“Average cost breakdown for Ooty vacation from major Indian cities.”**

#### Observation
Transportation from major cities costs around **50–300 INR per person.**

</details>

<details>
<summary><b>Loop 2: Transportation Planning</b></summary>

#### Thought
Transportation will be a significant portion of the total cost based on the starting location.



#### Action
Search for **"Cheapest transportation to Ooty from Bangalore/Chennai/Delhi."**


#### Observation
From Bangalore: Bus (1,800 INR round-trip for three) + additional expenses — exceeds budget allocation.

</details>

<details>
<summary><b>Loop 3: Accommodation Research</b></summary>

#### Thought
With approximately 7,000 INR remaining for accommodation, the budget allows for about 2,300 INR per night.



#### Action
Search for **"Budget hotels in Ooty under 2,500 INR with good reviews."**



#### Observation
Several options available: around 2,000–2,300 INR per night with an average rating of 8.5/10.

</details>

<b>Agent Outcome</b>

- Day-wise itinerary
- Booked flights and hotels
- Budget breakdown
- Travel and food recommendations
- Reminders and confirmations