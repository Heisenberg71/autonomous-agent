from .llm import call_llm
from .tools import tools, calculator

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
            city = plan[ARGS_KEY][CITY_KEY]
            temperature = tools.get_temperature(city)
            return f"{temperature} C"
        if plan[TOOL_KEY] == KNOWLEDGE_BASE:
            return tools.search_from_knowledge_base(plan[ARGS_KEY][QUERY_KEY])

    return str(plan)