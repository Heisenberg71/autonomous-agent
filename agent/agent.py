from .llm import call_llm, call_llm_with_knowledge_base
from .tools import tools, calculator, weather

# Tool names
CALCULATOR = "calculator"
WEATHER = "weather"
KNOWLEDGE_BASE = "kb"

# Plan keys
TOOL_KEY = "tool"
ARGS_KEY = "args"
EXPRESSION_KEY = "expr"
CITY_KEY = "city"
QUERY_KEY = "q"

def process_user_query(user_query):
    plan = call_llm(user_query)
    
    if plan and isinstance(plan, dict) and TOOL_KEY in plan:
        if plan[TOOL_KEY] == CALCULATOR:
            return calculator.calculate(plan[ARGS_KEY])
        if plan[TOOL_KEY] == WEATHER:
            weatherHistory = weather.getWeather(plan[ARGS_KEY])
            return call_llm_with_knowledge_base(user_query, weatherHistory)
        if plan[TOOL_KEY] == KNOWLEDGE_BASE:
            return tools.search_from_knowledge_base(plan[ARGS_KEY][QUERY_KEY])

    return str(plan)