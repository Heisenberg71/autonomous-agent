import sys
import os
import pytest

# Add src/ to sys.path so imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../src")))

from agent.tools.calculator import (
    calculate,
    generate_response,
    use_calculator_tool,
    OPERATOR_1,
    OPERATOR_2,
    OPERAND,
)

# ---------- Tests for calculate ----------
def test_addition():
    args = {OPERAND: "+", OPERATOR_1: 5, OPERATOR_2: 3}
    assert calculate(args) == 8.0

def test_subtraction():
    args = {OPERAND: "-", OPERATOR_1: 10, OPERATOR_2: 4}
    assert calculate(args) == 6.0

def test_multiplication():
    args = {OPERAND: "*", OPERATOR_1: 7, OPERATOR_2: 6}
    assert calculate(args) == 42.0

def test_division():
    args = {OPERAND: "/", OPERATOR_1: 8, OPERATOR_2: 2}
    assert calculate(args) == 4.0

def test_division_by_zero():
    args = {OPERAND: "/", OPERATOR_1: 5, OPERATOR_2: 0}
    assert calculate(args) == float("inf")

def test_percentage():
    args = {OPERAND: "%", OPERATOR_1: 20, OPERATOR_2: 50}
    assert calculate(args) == 10.0

def test_invalid_operand():
    args = {OPERAND: "invalid", OPERATOR_1: 5, OPERATOR_2: 3}
    result = calculate(args)
    assert isinstance(result, str)
    assert "Invalid operand" in result

def test_missing_operand_key():
    args = {OPERATOR_1: 5, OPERATOR_2: 3}
    result = calculate(args)
    assert isinstance(result, str)
    assert "Missing required field: operand" in result

def test_missing_operator1_key():
    args = {OPERAND: "+", OPERATOR_2: 3}
    result = calculate(args)
    assert isinstance(result, str)
    assert "Missing required field: operator_1" in result

def test_missing_operator2_key():
    args = {OPERAND: "+", OPERATOR_1: 5}
    result = calculate(args)
    assert isinstance(result, str)
    assert "Missing required field: operator_2" in result

def test_invalid_operator_value_type():
    args = {OPERAND: "+", OPERATOR_1: "five", OPERATOR_2: 3}
    result = calculate(args)
    assert isinstance(result, str)
    assert "Invalid values" in result

# ---------- Tests for generate_response ----------
def test_generate_response_with_number():
    assert generate_response(15) == "The result of the calculation is: 15"

def test_generate_response_with_error_message():
    error_message = "Invalid values: something went wrong"
    assert generate_response(error_message) == f"The result of the calculation is: {error_message}"

# ---------- Tests for use_calculator_tool ----------
def test_use_calculator_tool_success():
    args = {OPERAND: "*", OPERATOR_1: 4, OPERATOR_2: 5}
    result = use_calculator_tool(args)
    assert "The result of the calculation is: 20.0" == result

def test_use_calculator_tool_error():
    args = {OPERAND: "invalid", OPERATOR_1: 4, OPERATOR_2: 5}
    result = use_calculator_tool(args)
    assert "Invalid operand" in result
