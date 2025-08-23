from .llm import planner
from .tools import calculator, weather, knowledge_loader, currency_converter

# Tool names
CALCULATOR = "calculator"
WEATHER = "weather"
KNOWLEDGE_BASE = "knowledge_base"
CURRENCY_CONVERTER = "currency_converter"

# Plan keys
TOOL_KEY = "tool"
ARGS_KEY = "args"
EXPRESSION_KEY = "expr"
CITY_KEY = "city"
QUERY_KEY = "query"

def process_user_query(user_query):
    plan = planner.initiate_planner(user_query)
    
    if plan and isinstance(plan, dict) and TOOL_KEY in plan:
        if plan[TOOL_KEY] == CALCULATOR:
            return calculator.use_calculator_tool(plan[ARGS_KEY])
        if plan[TOOL_KEY] == WEATHER:
            weather_history = weather.get_weather_details(plan[ARGS_KEY])
            return planner.call_llm_with_knowledge_base(user_query, weather_history)
        if plan[TOOL_KEY] == KNOWLEDGE_BASE:
            titles = knowledge_loader.get_all_titles()
            top_matched_titles = planner.find_top_matched_titles(plan[ARGS_KEY][QUERY_KEY], titles)
            top_matched_knowledge = knowledge_loader.search_titles_and_details(top_matched_titles)
            return planner.call_llm_with_knowledge_base(user_query, top_matched_knowledge)
        if plan[TOOL_KEY] == CURRENCY_CONVERTER:
            return currency_converter.convert_currency(plan[ARGS_KEY])
    return "Sorry, I couldn't understand your request."