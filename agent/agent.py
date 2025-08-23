from .llm import call_llm, call_llm_with_knowledge_base, call_llm_with_titles_from_knowledge_base
from .tools import tools, calculator, weather, knowledge_loader

# Tool names
CALCULATOR = "calculator"
WEATHER = "weather"
KNOWLEDGE_BASE = "knowledge_base"

# Plan keys
TOOL_KEY = "tool"
ARGS_KEY = "args"
EXPRESSION_KEY = "expr"
CITY_KEY = "city"
QUERY_KEY = "query"

def process_user_query(user_query):
    plan = call_llm(user_query)
    
    if plan and isinstance(plan, dict) and TOOL_KEY in plan:
        if plan[TOOL_KEY] == CALCULATOR:
            return calculator.calculate(plan[ARGS_KEY])
        if plan[TOOL_KEY] == WEATHER:
            weatherHistory = weather.getWeather(plan[ARGS_KEY])
            return call_llm_with_knowledge_base(user_query, weatherHistory)
        if plan[TOOL_KEY] == KNOWLEDGE_BASE:
            titles = knowledge_loader.get_all_titles()
            top_matched_titles = call_llm_with_titles_from_knowledge_base(plan[ARGS_KEY][QUERY_KEY], titles)
            top_matched_knowledge = knowledge_loader.search_titles_and_details(top_matched_titles)
            return call_llm_with_knowledge_base(user_query, top_matched_knowledge)
        
    return str(plan)