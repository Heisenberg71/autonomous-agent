import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add src/ to sys.path so imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../src")))

from agent.agent import process_user_query

class TestProcessUserQuery(unittest.TestCase):

    @patch("agent.agent.calculator")
    @patch("agent.agent.weather")
    @patch("agent.agent.knowledge_loader")
    @patch("agent.agent.currency_converter")
    @patch("agent.agent.planner")
    def test_calculator_tool(self, mock_planner, mock_currency, mock_knowledge, mock_weather, mock_calculator):
        # Mock planner response for calculator
        mock_planner.initiate_planner.return_value = {
            "tool": "calculator",
            "args": {"operand": "%", "operator_1": 12.5, "operator_2": 243}
        }
        # Mock calculator tool
        mock_calculator.use_calculator_tool.return_value = "The result of the calculation is: 30.75"

        # Call the function
        result = process_user_query("What is 12.5% of 243?")

        # Assertions
        mock_planner.initiate_planner.assert_called_once_with("What is 12.5% of 243?")
        mock_calculator.use_calculator_tool.assert_called_once_with({
            "operand": "%", "operator_1": 12.5, "operator_2": 243
        })
        self.assertEqual(result, "The result of the calculation is: 30.75")

    @patch("agent.agent.calculator")
    @patch("agent.agent.weather")
    @patch("agent.agent.knowledge_loader")
    @patch("agent.agent.currency_converter")
    @patch("agent.agent.planner")
    def test_weather_tool(self, mock_planner, mock_currency, mock_knowledge, mock_weather, mock_calculator):
        # Mock planner response for weather
        mock_planner.initiate_planner.return_value = {
            "tool": "weather",
            "args": {"city": "Dhaka", "from_date": "2024-01-01", "to_date": "2024-01-02"}
        }
        # Mock weather tool
        mock_weather.get_weather_details.return_value = {"temp": 25, "condition": "Sunny"}
        # Mock planner's LLM call
        mock_planner.call_llm_with_knowledge_base.return_value = "Weather is sunny with 25°C"

        result = process_user_query("Tell me the weather in Dhaka")

        mock_weather.get_weather_details.assert_called_once_with({
            "city": "Dhaka", "from_date": "2024-01-01", "to_date": "2024-01-02"
        })
        mock_planner.call_llm_with_knowledge_base.assert_called_once()
        self.assertEqual(result, "Weather is sunny with 25°C")

    @patch("agent.agent.calculator")
    @patch("agent.agent.weather")
    @patch("agent.agent.knowledge_loader")
    @patch("agent.agent.currency_converter")
    @patch("agent.agent.planner")
    def test_knowledge_base_tool(self, mock_planner, mock_currency, mock_knowledge, mock_weather, mock_calculator):
        # Mock planner response for knowledge base
        # Arrange
        mock_planner.initiate_planner.return_value = {
            "tool": "knowledge_base",
            "args": {"query": "Python decorators"}
        }
        mock_knowledge.get_all_titles.return_value = ["Python Basics", "Python Decorators"]
        mock_planner.find_top_matched_titles.return_value = ["Python Decorators"]
        mock_knowledge.search_titles_and_details.return_value = [{"title": "Python Decorators", "details": "Example details"}]
        mock_planner.call_llm_with_knowledge_base.return_value = "Decorators allow wrapping functions"

        # Act
        result = process_user_query("Tell me about Python decorators")

        # Arrange
        mock_knowledge.get_all_titles.assert_called_once()
        mock_planner.find_top_matched_titles.assert_called_once_with("Python decorators", ["Python Basics", "Python Decorators"])
        mock_knowledge.search_titles_and_details.assert_called_once_with(["Python Decorators"])

        # Assert
        self.assertEqual(result, "Decorators allow wrapping functions")

    @patch("agent.agent.calculator")
    @patch("agent.agent.weather")
    @patch("agent.agent.knowledge_loader")
    @patch("agent.agent.currency_converter")
    @patch("agent.agent.planner")
    def test_currency_converter_tool(self, mock_planner, mock_currency, mock_knowledge, mock_weather, mock_calculator):
        # Mock planner response for currency converter
        # Arrange
        mock_planner.initiate_planner.return_value = {
            "tool": "currency_converter",
            "args": {"amount": 100, "from_currency": "USD", "to_currency": "EUR"}
        }
        mock_currency.convert_currency.return_value = "Converted amount: 92 EUR"

        # Act
        result = process_user_query("Convert 100 USD to EUR")
        mock_currency.convert_currency.assert_called_once_with({"amount": 100, "from_currency": "USD", "to_currency": "EUR"})

        # Assert
        self.assertEqual(result, "Converted amount: 92 EUR")

    @patch("agent.agent.planner")
    def test_unknown_tool(self, mock_planner):
        # Planner returns something unexpected
        # Arrange
        mock_planner.initiate_planner.return_value = {"tool": "unknown"}

        # Act
        result = process_user_query("Do something weird")

        # Assert
        self.assertEqual(result, "Sorry, I couldn't understand your request.")