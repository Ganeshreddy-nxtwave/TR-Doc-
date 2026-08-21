# Building_an_AI_Agent_from_Scratch_TR_Doc_FINAL

# Building an AI Agent from Scratch

**Course:** Building LLM Applications

**Topic:** Building an AI Agent from Scratch

---

# Building an AI Agent from Scratch

## Introduction

In the previous unit we learned **Tool Use & Function Calling**. We gave an LLM a `get_weather` function, the model returned a tool call, we executed the function ourselves, and we sent the result back so the model could answer in natural language.

In this unit we will ask that code one realistic question — and watch it fail. Fixing that failure is what turns function calling into an **AI Agent**, and we will build it with only `requests` and the Gemini SDK, using **no LangChain, LlamaIndex** 

---

## Recap: What We Built Last Unit

| Step | What we did |
| --- | --- |
| 1 | Created the Python function that fetches the information |
| 2 | Defined the tool using a JSON schema so the LLM knows it exists |
| 3 | Handled the tool call returned by the LLM and executed the function |
| 4 | Sent the tool output back to the LLM for a natural language answer |

```
question + tools  ->  tool call  ->  we execute it  ->  send result back -> final answer
```

The LLM never executes the function. It only decides **which** tool to call and **with what arguments**. We run the code.

---

## The Hook: Where Function Calling Stops

Here is a question a real traveller would ask:

> *“I’m in Hyderabad and want to visit Tirupati tomorrow. Check the weather there, find me a flight, and suggest a hotel.”*
> 

Suppose we have written all three functions — `get_weather`, `get_flights` and `get_hotels` — and described all three to the model. Now we run our function calling code from the previous unit.

### What Actually Happens

| The code does | The result |
| --- | --- |
| Sends the question with all three tools | The model asks for `get_weather` |
| Runs `get_weather` and sends the result back | Good so far |
| Asks the model once more | The model asks for `get_flights` |
| **Nothing** — our code has already finished | The flight and hotel answers never arrive |

The user gets a partial answer about the weather, and nothing else.

### Why It Fails

Our code handled **one** tool call because we **wrote** one. The number of steps was fixed the moment we typed it — before any user asked anything.

We could paste the handling block a second time, and a third. That works for this question. But now consider:

> *“Compare the weather in Tirupati and Vizag, pick the cooler city, and find me a hotel there.”*
> 

How many blocks should we paste this time?

- Two weather calls, then one hotel call — three blocks?
- What if the user names four cities?
- And notice: **the hotel call cannot be written in advance at all**, because the city is unknown until both weather results come back.

### The Question That Changes Everything

> Our code ran one tool because **we** decided one call.
For this question, **how many calls should there be — and who can possibly know?**
> 

Not us. We cannot know in advance, because the answer depends on results that do not exist yet.

**Only the model can know** — and only after seeing each result.

### What That Forces Us to Change

| What we must add | Why |
| --- | --- |
| More than one tool | One question can need weather, flights and hotels |
| A growing conversation | Each decision must be made with all previous results in view |
| A loop instead of fixed blocks | We stop counting steps; the model keeps going until the goal is reached |

That is the whole of this unit. And the thing we get when we add those three is called an **AI Agent**.

---

## So What Is an AI Agent?

> An **AI agent** is a system that can operate independently to achieve a specific goal without constant human intervention.
> 

The key word is **independently**. In function calling, we decided the steps. In an agent, the model decides.

### Core Components

| Component | Role | In our build |
| --- | --- | --- |
| AI Model | The brain — understands the goal and decides what to do | Gemini |
| Tools | The arms and legs — fetch real data | `get_weather`, `get_hotels`, `get_flights` |
| Memory | Keeps context so decisions build on earlier results | The `llm_messages` list |

Two of these you already have from function calling — a model and a tool. What an agent adds is **memory that carries across rounds**, and a **loop** driven by the model rather than by us.

### The ReAct Pattern

Agents commonly follow **ReAct** — *Reason, Act, Observe* — repeated in a loop:

| Stage | What happens |
| --- | --- |
| **Thought / Reason** | The model decides what it needs next |
| **Action** | The model calls a tool |
| **Observation** | The model sees the tool output and re-evaluates |

The three stages repeat until the model produces a final **Answer** instead of another tool call.

### Function Calling vs AI Agent

|  | Function Calling | AI Agent |
| --- | --- | --- |
| Tool calls | Exactly one | As many as needed |
| Number of rounds | Fixed by our code | Decided by the model at runtime |
| Tool selection | Only one tool available | Chooses between multiple tools |
| Dependent steps | Not possible | Later calls use earlier results |
| Memory | Within one exchange | Carried across every round |
| Control flow | Straight-line code | Loop with a stopping condition |
| Stops when | The code finishes | The goal is reached |

---

## Let’s Build: A Travel Assistant Agent

### The User’s Problem

Planning even a short trip means visiting several sites and holding the results in your head:

| The traveller wants to know | Where they look today |
| --- | --- |
| Will the weather be good? | A weather site |
| How do I get there? | A flight booking site |
| Where do I stay? | A hotel booking site |

Each site answers only its own question. Nothing connects them. If the weather turns out to be bad, the traveller starts again with a different city — and repeats all three searches.

### What Our Agent Will Do

The user asks **one question in plain English**, and the agent decides which tools to call, calls them, reads the results, and replies with one combined answer.

- **One question instead of three searches** — no switching between sites
- **The results are connected** — the agent can skip the hotel search if the weather is bad
- **It handles the details** — the user says “Hyderabad”, the agent sends `HYD` to the flight tool
- **It reports honestly** — if a tool fails, the agent says so instead of inventing an answer

Our tools only **search**. They do not book, pay or reserve anything. Read-only tools are safe for an agent to run automatically. Tools that take real action — booking, paying, sending, deleting — need a human confirmation step before they run.

### Building Without a Framework

Frameworks such as LangChain provide this loop through a single method call. They are useful, but they hide the mechanism. We write it ourselves because:

- The agent loop is roughly **20 lines of Python** — it is worth seeing in full
- You understand exactly **when** the model is called and **what** is sent to it
- Debugging is simple — you can print every round
- The same pattern works with **any** LLM provider

### Agent Core Components

| Component | Purpose |
| --- | --- |
| Google Gemini | AI reasoning and decision-making |
| Open-Meteo API | Current weather and rain forecast |
| Serp API — Google Hotels | Live hotel names, prices and ratings |
| Serp API — Google Flights | Live airlines, timings and fares |
| Python loop | Orchestrates the agent — replaces the framework |

### Prerequisites

- A [**Gemini API Key**](https://aistudio.google.com/apikey) to access the model
- A [**Serp API Key**](https://serpapi.com/manage-api-key) to fetch flight and hotel data
- Python environment with the `google-genai` and `requests` packages installed

The Open-Meteo weather API requires **no API key**. Store your Gemini and Serp API keys in Colab Secrets as `GEMINI_API_KEY` and `SERPAPI_KEY` — never paste keys directly into the code.

---

## Steps to Build the Agent

1. Setting Up the Gemini Client
2. Defining the Tools and System Instruction
    1. Creating the Weather Function
    2. Creating the Hotel Function
    3. Creating the Flight Function
3. Handling a Single Tool Call
4. Building the Agent Loop
5. Executing the Agent

---

## Step 1: Setting Up the Gemini Client

### Install Dependencies

```bash
!pip -q install -U google-genai requests
```

### Initialise the Client and Model

We create one `client` object and store the model name in a constant, so a model change later is a one-line edit.

- **Code**
    
    ```python
    from google.colab import userdata
    from google import genai
    from google.genai import types
    import json, requests
    
    client = genai.Client(api_key=userdata.get('GEMINI_API_KEY'))
    
    MODEL = "gemini-3.5-flash-lite"
    
    print(client.models.generate_content(model=MODEL, contents="say: setup works").text)
    ```
    

### Confirming the Knowledge Cutoff

Before adding tools, let us confirm the limitation that makes them necessary.

```python
response = client.models.generate_content(
    model=MODEL,
    contents="What is the current weather in Hyderabad",
)
print(response.text)
```

The model cannot answer. It has no access to live data — only what was present in its training data.

---

## Step 2: Defining the Tools and System Instruction

Our agent needs three abilities. We will build each one as a normal Python function first, then describe all three to the model, and only then write the system instruction that governs how they are used.

---

### Step 2.1: Creating the Weather Function

We use **Open-Meteo**, which is free and needs no key. It works on latitude and longitude, so before we can ask for weather we need to turn a city name into coordinates.

#### Resolving a City to Coordinates

Open-Meteo’s geocoding endpoint takes a place name and returns matching locations. One detail matters: many places share a name — there are several villages in India called Patna. If we take the first result we may get a village instead of the city.

So we ask for 10 results, keep the Indian ones, and pick the most populous.

- **Code**
    
    ```python
    def find_place(location):
        results = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": location, "count": 10},
            timeout=10,
        ).json().get("results", [])
    
        if not results:
            return None
    
        indian = [place for place in results if place.get("country_code") == "IN"]
    
        # many places share a name - take the most populous match
        return max(indian or results, key=lambda place: place.get("population", 0) or 0)
    
    print(find_place("Hyderabad"))
    print(find_place("Patna"))
    ```
    

The `or results` fallback means non-Indian cities such as London and Paris still work normally.

#### Understanding the Weather API Parameters

| Parameter | Description | Example |
| --- | --- | --- |
| `latitude`, `longitude` | Location coordinates | `17.38`, `78.45` |
| `current` | Which live readings we want | `temperature_2m,weather_code` |
| `daily` | Which daily forecast values we want | `precipitation_probability_max` |
| `timezone` | Ensures times match the location | `auto` |

Open-Meteo returns the sky condition as a **number** — `0`, `3`, `61` and so on. The LLM cannot read that, so we keep a dictionary that converts the code into words.

#### Returning the Required Weather Info

The function does three things: find the place, call the API, and return a small dictionary. If the place cannot be found, it returns an `error` key instead of crashing.

- **Code**
    
    ```python
    WEATHER_CODES = {
        0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
        45: "fog", 48: "freezing fog", 51: "light drizzle", 53: "drizzle",
        55: "heavy drizzle", 61: "light rain", 63: "moderate rain", 65: "heavy rain",
        71: "light snow", 73: "snow", 75: "heavy snow", 80: "rain showers",
        81: "moderate rain showers", 82: "violent rain showers",
        95: "thunderstorm", 96: "thunderstorm with hail", 99: "severe thunderstorm",
    }
    
    def get_weather(location):
        place = find_place(location)
    
        if place is None:
            return {"error": f"Could not find a place called '{location}'"}
    
        data = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": place["latitude"], "longitude": place["longitude"],
                "current": "temperature_2m,relative_humidity_2m,weather_code",
                "daily": "precipitation_probability_max",
                "forecast_days": 1, "timezone": "auto",
            },
            timeout=10,
        ).json()
    
        current = data["current"]
    
        return {
            "location": place["name"],
            "temperature": current["temperature_2m"],
            "description": WEATHER_CODES.get(current["weather_code"], "unknown"),
            "humidity": current["relative_humidity_2m"],
            "rain_chance_today": data["daily"]["precipitation_probability_max"][0],
        }
    
    print(get_weather("Hyderabad"))
    print(get_weather("Zzzxqq"))          # error path
    ```
    
- **Output**
    
    ```python
    {'location': 'Hyderabad', 'temperature': 25.2, 'description': 'overcast',
     'humidity': 81, 'rain_chance_today': 81}
    
    {'error': "Could not find a place called 'Zzzxqq'"}
    ```
    

Notice the function returns a **small, clean dictionary** — not the full raw API response. The LLM reads this output, so removing unnecessary fields keeps the model focused and reduces token usage.

---

### Step 2.2: Creating the Hotel Function

Weather alone cannot answer a travel question. To recommend where to stay, the agent needs live hotel data.

#### Understanding Serp API

Serp API returns structured JSON from Google’s search products. We use its **Google Hotels** engine, which gives hotel names, prices per night, star ratings and review counts.

| Parameter | Description | Example |
| --- | --- | --- |
| `engine` | Which Google product to query | `"google_hotels"` |
| `q` | Free-form hotel search query | `"hotels in Tirupati"` |
| `check_in_date` | Check-in date in YYYY-MM-DD | `"2026-08-14"` |
| `check_out_date` | Check-out date in YYYY-MM-DD | `"2026-08-16"` |
| `currency` | Currency for prices | `"INR"` |
| `gl` | Country code for results | `"in"` |

#### Handling the Dates

Hotels need check-in and check-out dates, but the user rarely gives them. Rather than asking the model to work out today’s date — something LLMs do unreliably — we calculate it in Python: check in tomorrow, check out two days later.

#### Creating the Hotel Function

The shape is the same as `get_weather`: call the API, check for an error, and return a trimmed dictionary of at most five hotels.

- **Code**
    
    ```python
    import datetime
    
    SERPAPI_KEY = userdata.get('SERPAPI_KEY')
    
    def get_hotels(location):
        check_in = datetime.date.today() + datetime.timedelta(days=1)
        check_out = check_in + datetime.timedelta(days=2)
    
        data = requests.get(
            "https://serpapi.com/search",
            params={
                "api_key": SERPAPI_KEY,
                "engine": "google_hotels",
                "q": f"hotels in{location}",
                "check_in_date": str(check_in),
                "check_out_date": str(check_out),
                "adults": 2, "currency": "INR", "gl": "in", "hl": "en",
            },
            timeout=30,
        ).json()
    
        if "error" in data:
            return {"error": data["error"]}
    
        hotels = data.get("properties", [])
    
        if not hotels:
            return {"error": f"No hotels found in{location}"}
    
        return {
            "location": location,
            "check_in": str(check_in),
            "check_out": str(check_out),
            "hotels": [
                {
                    "name": hotel.get("name"),
                    "price_per_night": hotel.get("rate_per_night", {}).get("lowest", "not listed"),
                    "rating": hotel.get("overall_rating"),
                    "hotel_class": hotel.get("hotel_class"),
                }
                for hotel in hotels[:5]
            ],
        }
    
    print(get_hotels("Tirupati"))
    ```
    

The `.get()` method retrieves data safely, returning a default if the field does not exist. This matters because not every hotel listing includes every field — some have no star rating, some have no price.

---

### Step 2.3: Creating the Flight Function

To complete the travel assistant, the agent also needs to find flights. We use the same Serp API key with a different engine — **Google Flights**.

| Parameter | Description | Example |
| --- | --- | --- |
| `engine` | Which Google product to query | `"google_flights"` |
| `departure_id` | Departure airport IATA code | `"HYD"` |
| `arrival_id` | Arrival airport IATA code | `"TIR"` |
| `outbound_date` | Travel date in YYYY-MM-DD | `"2026-08-14"` |
| `type` | 1 = round trip, 2 = one way | `2` |
| `currency` | Currency for fares | `"INR"` |

#### A Design Decision: Airport Codes

Google Flights needs **airport codes**, not city names. `"Hyderabad"` returns nothing; `"HYD"` works. We have two options:

| Option | Result |
| --- | --- |
| Build a city-to-airport lookup table in our code | More code, and only the airports we remember to add |
| Let the **model** supply the code | No extra code, and it already knows every airport |

We choose the second. This is why this tool takes **two parameters** — `from_airport` and `to_airport` — while the other two take one.

#### Creating the Flight Function

Serp API returns flights in two lists, `best_flights` and `other_flights`, so we take the first and fall back to the second. Each option contains a list of legs; the first leg holds the departure and the last holds the arrival, which is how we count stops.

- **Code**
    
    ```python
    def get_flights(from_airport, to_airport):
        outbound = datetime.date.today() + datetime.timedelta(days=1)
    
        data = requests.get(
            "https://serpapi.com/search",
            params={
                "api_key": SERPAPI_KEY,
                "engine": "google_flights",
                "departure_id": from_airport,
                "arrival_id": to_airport,
                "outbound_date": str(outbound),
                "type": 2,                          # 2 = one way
                "currency": "INR", "gl": "in", "hl": "en",
            },
            timeout=30,
        ).json()
    
        if "error" in data:
            return {"error": data["error"]}
    
        flights = data.get("best_flights", []) or data.get("other_flights", [])
    
        if not flights:
            return {"error": f"No flights found from{from_airport} to{to_airport}"}
    
        return {
            "from": from_airport,
            "to": to_airport,
            "date": str(outbound),
            "flights": [
                {
                    "airline": option["flights"][0].get("airline"),
                    "flight_number": option["flights"][0].get("flight_number"),
                    "departure": option["flights"][0]["departure_airport"].get("time"),
                    "arrival": option["flights"][-1]["arrival_airport"].get("time"),
                    "duration_minutes": option.get("total_duration"),
                    "stops": len(option["flights"]) - 1,
                    "price": option.get("price"),
                }
                for option in flights[:5]
            ],
        }
    
    print(get_flights("HYD", "TIR"))
    ```
    
- **Output**
    
    ```python
    {'from': 'HYD', 'to': 'TIR', 'date': '2026-08-14', 'flights': [
      {'airline': 'Star Air', 'flight_number': 'S5 212', 'duration_minutes': 170,
       'stops': 1, 'price': 10354},
      {'airline': 'Air India', 'flight_number': 'AI 2859', 'duration_minutes': 70,
       'stops': 0, 'price': 15600},
      {'airline': 'IndiGo', 'flight_number': '6E 7503', 'duration_minutes': 85,
       'stops': 0, 'price': 18210},
      {'airline': 'Alliance Air', 'flight_number': '9I 877', 'duration_minutes': 85,
       'stops': 0, 'price': None}
    ]}
    ```
    
    The cheapest option has a stop and takes the longest. One listing has `price: None` — not every flight has a fare attached, which is why `.get()` is used throughout.
    

---

### All Three Tools Share the Same Shape

|  | `get_weather` | `get_hotels` | `get_flights` |
| --- | --- | --- | --- |
| Input | `location` | `location` | `from_airport`, `to_airport` |
| Data source | Open-Meteo | Serp API | Serp API |
| Returns | Small dictionary | Small dictionary | Small dictionary |
| On failure | `error` key | `error` key | `error` key |

Any tool you add later should follow this same pattern.

---

### Describing the Tools to the LLM

Our functions exist, but the model still does not know about them. As in the previous unit, we describe each one using a **JSON schema**.

| Field | Purpose |
| --- | --- |
| `name` | Function name the LLM will call |
| `description` | What the function does — this is how the model decides *when* to use it |
| `parameters` | What inputs the function needs |
| `properties` | Details about each parameter |
| `required` | Which parameters are mandatory |
- **Code**
    
    ```python
    weather_declaration = {
        "name": "get_weather",
        "description": "Get current weather for a city - temperature, conditions, humidity and rain chance. Use for weather, temperature, rain, or what to wear.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name like Hyderabad, Mumbai, London"}
            },
            "required": ["location"],
        },
    }
    
    hotel_declaration = {
        "name": "get_hotels",
        "description": "Find hotels in a city with price per night, star rating and review count. Use whenever the user asks about hotels, where to stay, or accommodation.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name like Tirupati, Goa, Jaipur"}
            },
            "required": ["location"],
        },
    }
    
    flight_declaration = {
        "name": "get_flights",
        "description": "Find flights between two airports for tomorrow, with airline, flight number, timings, stops and price. Use whenever the user asks about flights or how to reach a city by air.",
        "parameters": {
            "type": "object",
            "properties": {
                "from_airport": {"type": "string", "description": "Departure airport IATA code, e.g. HYD for Hyderabad"},
                "to_airport": {"type": "string", "description": "Arrival airport IATA code, e.g. TIR for Tirupati"},
            },
            "required": ["from_airport", "to_airport"],
        },
    }
    ```
    

The `description` field is the most important line you will write. With three tools available, the model chooses between them **entirely based on their descriptions**. A vague description leads to the wrong tool being called.

---

### Writing the System Instruction

The model now knows **what** each tool does. It still does not know **how we want it to behave** — how carefully to work, what to do when a tool fails, or whether it is allowed to guess.

With one tool this barely mattered. With three tools it becomes the difference between an agent that works and one that invents answers.

| The instruction must tell the model | Why it matters with three tools |
| --- | --- |
| Always call a tool, never invent information | More tools means more chances to guess |
| Some questions need more than one tool call | Otherwise it answers after the first tool |
| Keep going until the goal is reached | This is what will drive our loop |
| Convert city names to airport codes | The flight tool needs `HYD`, not `Hyderabad` |
| Report tool errors instead of retrying | Prevents wasted rounds on a failed tool |
| Search only, never claim a booking | Our tools cannot book anything |
- **Code**
    
    ```python
    SYSTEM_PROMPT = """You are a friendly weather and travel assistant for users in India.
    
    Rules:
    - NEVER invent weather, flight or hotel information. Always call a tool to get it.
    - Only mention a city's temperature if you actually called the weather tool for it.
    - If the user names a state or region, use its main city instead
      (Goa -> Madgaon, Kerala -> Kochi) and tell the user which city you used.
    - Many questions need MORE THAN ONE tool call. Work step by step: call a tool,
      look at the result, and if the user's goal is not fully answered yet, call the
      next tool. Give your final answer only once the goal is reached.
    - When listing hotels, give the hotel name, price per night and rating.
    - Hotel prices are in INR, for a 2-night stay starting tomorrow.
    - If a tool returns an error, report it to the user immediately. Do NOT call the
      same tool again with reworded arguments - the error is not caused by the wording.
    - Keep the final answer short and friendly.
    - Use official city names when calling tools (Bangalore -> Bengaluru,
      Bombay -> Mumbai, Calcutta -> Kolkata, Madras -> Chennai).
    - For flights, convert city names to IATA airport codes yourself
      (Hyderabad -> HYD, Tirupati -> TIR, Bengaluru -> BLR, Delhi -> DEL).
    - Flights and hotels are for a trip starting tomorrow.
    - You can search for flights and hotels, but you cannot book or reserve anything.
      Never tell the user something has been booked.
    """
    ```
    

### Configuring the Model

Both the tool descriptions and the system instruction are passed to the model in a single `config` object, which we will reuse on every request.

```python
config = types.GenerateContentConfig(
    tools=[types.Tool(function_declarations=[
        weather_declaration,
        hotel_declaration,
        flight_declaration,
    ])],
    system_instruction=SYSTEM_PROMPT,
)

print("3 tools described to the model.")
```

---

## Step 3: Handling a Single Tool Call

Before building the loop, let us confirm that one round works. This is the flow from the previous unit, written in Gemini syntax — and it is the block we will soon put inside a loop.

### Chat Completion Request

We send the question together with the `config` that carries the tools. Note that `llm_messages` is a **list** — this is the conversation the model sees, and it will grow as the agent works.

- **Code**
    
    ```python
    llm_messages = [
        types.Content(role="user", parts=[types.Part(text="What is the weather in Mumbai?")])
    ]
    
    response = client.models.generate_content(
        model=MODEL, contents=llm_messages, config=config,
    )
    
    print("text :", response.text)
    print("calls:", response.function_calls)
    ```
    

### Understanding the LLM Response

The output shows that `response.text` is **empty**, while `response.function_calls` is **populated**.

The model did not answer the question. It returned a structured request meaning: *“run `get_weather` with `location = Mumbai` and tell me the result.”*

When the LLM decides to use a tool, it returns:

- The **function name** to call
- The **arguments** to use
- A tool call **id**

Notice also that the model picked `get_weather` out of **three** available tools, purely from the descriptions.

### Executing the Tool Call and Returning the Output

Now we run the function ourselves and add two things to the conversation: what the model asked for, and what our tool returned. The `id` links our output back to the specific call the model made.

- **Code**
    
    ```python
    response_message = response.candidates[0].content
    
    if response.function_calls:
        tool_call = response.function_calls[0]
        arguments = dict(tool_call.args)
        location = arguments["location"]
    
        print(f"LLM wants weather for:{location}")
    
        weather_data = get_weather(location)                 # WE run it
    
        llm_messages.append(response_message)                # what the model asked for
        llm_messages.append(types.Content(role="user", parts=[
            types.Part(function_response=types.FunctionResponse(
                name=tool_call.name,
                response={"result": weather_data},
                id=tool_call.id,
            ))
        ]))
    
        final_response = client.models.generate_content(
            model=MODEL, contents=llm_messages, config=config,
        )
        print(final_response.text)
    ```
    

This works — but only for a question that needs exactly one tool, exactly once. This is precisely where our traveller’s question broke.

---

## Step 4: Building the Agent Loop

We now fix that break. The plan is simple: repeat the block above **until the model stops asking for tools**.

```
repeat:
    ask the model
    if it did not ask for a tool  ->  we have the answer, stop
    otherwise                     ->  run the tools, send the results back
```

We will build this one piece at a time.

### The Tool Registry

The model returns a tool name as a **string** — `"get_weather"`. We need a way to turn that string into the actual Python function.

```python
TOOLS = {
    "get_weather": get_weather,
    "get_hotels": get_hotels,
    "get_flights": get_flights,
}
```

Now `TOOLS["get_weather"]` gives us the function itself, and `TOOLS["get_weather"](location="Mumbai")` runs it.

### Piece 1: Start the Conversation and Repeat

The conversation starts with the user’s question. Everything else gets appended to it as the agent works — this list is the agent’s **memory**.

```python
def run_agent(question, max_steps=6):
    llm_messages = [types.Content(role="user", parts=[types.Part(text=question)])]

    for step in range(max_steps):
        ...
```

`max_steps` is a safety limit. Without it, a confused model could keep calling tools forever.

### Piece 2: Ask the Model

Inside the loop we send the **entire conversation so far** — not just the original question. Without this, the model would have no idea what it already asked, and would request the same tool every round.

```python
        response = client.models.generate_content(
            model=MODEL, contents=llm_messages, config=config,
        )
```

### Piece 3: The Stopping Condition

If the model did not ask for a tool, it has produced its final answer. The goal is reached, so we return and stop looping.

```python
        if not response.function_calls:
            return response.text
```

This single line is the answer to the question we asked at the start of this unit. We no longer decide how many tool calls there will be — **the model tells us when it is done**.

### Piece 4: Remember What the Model Asked For

If we skip this, the next round has no record of the request, and the model asks for the same thing again.

```python
        llm_messages.append(response.candidates[0].content)
```

### Piece 5: Run Every Requested Tool

The model may ask for **several tools in one response**, so we loop over `response.function_calls` rather than taking only the first.

```python
        parts = []
        for call in response.function_calls:
            print(f"  [round{step + 1}]{call.name}({dict(call.args)})")

            if call.name not in TOOLS:
                result = {"error": "No such tool: " + call.name}
            else:
                try:
                    result = TOOLS[call.name](**call.args)
                except Exception as error:
                    result = {"error": str(error)}
```

Two protections here:

- If the model invents a tool name that does not exist, we return an error instead of crashing
- If a tool raises an exception, `try / except` turns it into an error message and the agent keeps working

### Piece 6: Send All Results Back

Each result is wrapped in a `FunctionResponse` and linked to its call by `id`. All results from this round go back in one message, and then the loop repeats.

```python
            parts.append(types.Part(function_response=types.FunctionResponse(
                name=call.name, response={"result": result}, id=call.id,
            )))

        llm_messages.append(types.Content(role="user", parts=parts))
```

### The Complete Agent Loop

- **Code**
    
    ```python
    TOOLS = {
        "get_weather": get_weather,
        "get_hotels": get_hotels,
        "get_flights": get_flights,
    }
    
    def run_agent(question, max_steps=6):
        llm_messages = [types.Content(role="user", parts=[types.Part(text=question)])]
    
        for step in range(max_steps):
    
            response = client.models.generate_content(
                model=MODEL, contents=llm_messages, config=config,
            )
    
            if not response.function_calls:
                return response.text                        # goal reached
    
            llm_messages.append(response.candidates[0].content)
    
            parts = []
            for call in response.function_calls:
                print(f"  [round{step + 1}]{call.name}({dict(call.args)})")
    
                if call.name not in TOOLS:
                    result = {"error": "No such tool: " + call.name}
                else:
                    try:
                        result = TOOLS[call.name](**call.args)
                    except Exception as error:
                        result = {"error": str(error)}
    
                parts.append(types.Part(function_response=types.FunctionResponse(
                    name=call.name, response={"result": result}, id=call.id,
                )))
    
            llm_messages.append(types.Content(role="user", parts=parts))
    
        return "Stopped: the agent hit the step limit without finishing."
    
    print("Agent ready with", len(TOOLS), "tools.")
    ```
    

### Understanding the Loop

| Line | What it does |
| --- | --- |
| `for step in range(max_steps)` | Hard limit on rounds — prevents an infinite loop |
| `if not response.function_calls` | No tool requested means the goal is reached |
| `llm_messages.append(...)` | Adds the tool call to memory so the next round has context |
| `for call in response.function_calls` | The model can request several tools in one round |
| `TOOLS[call.name](**call.args)` | Looks up the function by name and passes the model’s arguments |
| `try / except` | A crashing tool becomes an error message, not a stopped agent |

---

### Multiple Tool Calls in One Round

In Piece 5 we looped over `response.function_calls` instead of taking only the first. That single decision is what lets the agent work efficiently.

|  | Parallel — same round | Sequential — separate rounds |
| --- | --- | --- |
| When | The calls are **independent** | A call **needs the previous result** |
| Model behaviour | Requests several tools at once | Requests one, waits, then requests the next |
| Rounds used | One | One per dependent step |
| Example | Weather, flight and hotel for the same city | Compare two cities, then search for the winner |

**Parallel** — *“Check the weather in Tirupati, find me a flight, and suggest a hotel.”* Nothing depends on anything else, because the destination is already known.

```
  [round 1] get_weather({'location': 'Tirupati'})
  [round 1] get_flights({'from_airport': 'HYD', 'to_airport': 'TIR'})
  [round 1] get_hotels({'location': 'Tirupati'})
```

**Sequential** — *“Compare Tirupati and Vizag, pick the cooler city, find a hotel there.”* The hotel city is unknown until both weather results are in.

```
  [round 1] get_weather({'location': 'Tirupati'})
  [round 1] get_weather({'location': 'Vizag'})
  [round 2] get_hotels({'location': 'Tirupati'})
```

The model decides which pattern to use. Our loop handles both without any change — it simply runs whatever tools arrive in each round.

### Adding a Tool Does Not Change the Loop

Adding a fourth tool means writing **one declaration dict** and **one line in `TOOLS`**. `run_agent` is not touched.

The loop is **generic** — it runs whatever is registered in `TOOLS`, however many there are.

---

## Step 5: Executing the Agent

### The Question We Started With

```python
print(run_agent("I'm in Hyderabad and want to visit Tirupati tomorrow. "
                "Check the weather there, find me a flight, and suggest a hotel."))
```

This is the question that broke our function calling code at the start of the unit. The agent now calls all three tools, converts *Hyderabad* to `HYD` and *Tirupati* to `TIR`, and returns one combined answer.

### Two Tools, Where the Second Depends on the First

```python
print(run_agent("I'm going to Tirupati this weekend. Check the weather there, "
                "and if it's not raining heavily, find me a hotel."))
```

The agent calls `get_weather` first. Only after observing that result can it decide whether to call `get_hotels`.

### A Goal the Agent Must Plan For

```python
print(run_agent("Compare the weather in Tirupati and Vizag, pick the cooler city, "
                "and then find me a hotel there under 4000 rupees a night."))
```

The model chose the number of rounds, the order of the calls, and the argument of the final call — all at runtime. This is the behaviour we could not have hard-coded.

### When No Tool Is Needed

```python
print(run_agent("Who are you and what can you help me with?"))
```

The model answers directly with no tool call, and the loop returns on the very first round. Tools are used **only when required**.

---

## Flow Summary

1. **Developer**: Defines `get_weather`, `get_hotels` and `get_flights` in Python
2. **Developer**: Describes all three functions to the LLM using JSON schemas
3. **Developer**: Writes the system instruction and registers the functions in `TOOLS`
4. **User**: Asks a question that may need several steps
5. **LLM**: Returns one or more tool calls
6. **Loop**: Executes each requested tool and appends the outputs to the conversation
7. **LLM**: Observes the tool outputs and decides — call another tool, or answer
8. **Loop**: Repeats steps 5–7 until the LLM returns text instead of a tool call
9. **LLM**: Produces the final natural language answer once the goal is reached

---

## Try It Yourself

Add a **fourth tool** to this same agent. The loop does not change at all:

1. Pick an API you want to use
2. Write a function that calls it and returns a small, clean dictionary
3. Write its JSON schema, with a clear `description`
4. Add the schema to `function_declarations` and the function to `TOOLS`
5. Ask a question that needs your new tool **plus** one of the existing tools

| Agent Type | Tools to Combine | What It Does |
| --- | --- | --- |
| Tech Event Agent | Events Search + Web Search | Find hackathons and meetups in a city |
| News Digest Agent | News API + Web Search | Fetch and summarise today’s headlines by topic |

Pick two tools where the **second call needs the first call’s answer**. If both could run at the same time, you have built a chatbot with two APIs — not an agent.

---

---