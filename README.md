# Autonomous Agent: Enhanced with Multiple Tools

## Introduction
An **AI-powered autonomous agent** designed to handle user queries using any configured **Large Language Model (LLM)**.  
To effectively respond to diverse user requests, the LLM can leverage various **specialized tools**.  
By intelligently selecting the appropriate tool, the agent ensures **efficient, accurate, and autonomous query handling**.

---

##  Available Tools
-  **Calculator** – Perform arithmetic and percentage calculations  
-  **Currency Converter** – Convert exchange rates in real time  
-  **Knowledge Source Loader** – Retrieve factual and structured information  
-  **Weather Forecaster** – Get up-to-date weather information  

---

##  External Services
- **Weather API** → Fetches real-time weather forecasts  
- **Exchangerate-API** → Provides accurate and current currency exchange rates  

---

##  Quick Start

###  Requirements
- Python **3.12+** (recommended)  
- Virtual environment for isolated dependencies  

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

###  Run Examples

```bash
python main.py "What is 12.5% of 243?"
python main.py "Summarize today's weather in Paris in 3 words"
python main.py "Who is Ada Lovelace?"
python main.py "Add 10 to the average temperature in Paris and London right now."
```

>  **Note:** As this project currently uses a **simulated LLM** instead of a real one,  
> responses must be manually configured in the `planner.py` file.  

---

###  Run Tests

```bash
pytest -q
```

---

 Now you're ready to explore the **Autonomous Agent** with tool-enhanced intelligence!
