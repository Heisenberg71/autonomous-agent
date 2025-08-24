import os
import sys
import importlib
from unittest.mock import patch, MagicMock
import pytest
import requests

# Add src/ to sys.path so imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../src")))

@pytest.fixture
def currency_module(monkeypatch):
    """
    Import the module only after ensuring EXCHANGE_RATE_API_KEY is present.
    This prevents import-time ValueError from the module.
    """
    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "test-key")

    # Force a clean re-import in case it was cached
    modname = "agent.tools.currency_converter"
    if modname in sys.modules:
        del sys.modules[modname]
    module = importlib.import_module(modname)
    return module


# --------- Success case ---------
def test_convert_currency_success(currency_module):
    with patch(f"{currency_module.__name__}.requests.get") as mock_get:
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"rates": {"EUR": 0.85, "USD": 1.0}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Act
        args = {"from_currency": "USD", "to_currency": "EUR", "amount": 100}
        result = currency_module.convert_currency(args)

        # Assert
        assert "amount is 85.0" in result
        assert "conversion rate is 0.85" in result
        mock_get.assert_called_once_with("https://api.exchangerate-api.com/v4/latest/USD")


# --------- Validation errors ---------
def test_missing_parameters(currency_module):
    args = {"from_currency": "USD"}  # missing to_currency and amount
    with pytest.raises(ValueError, match="Missing required parameters"):
        currency_module.convert_currency(args)

def test_negative_amount(currency_module):
    args = {"from_currency": "USD", "to_currency": "EUR", "amount": -5} # negative amount
    with pytest.raises(ValueError, match="Amount must be positive"):
        currency_module.convert_currency(args)

def test_invalid_currency_code(currency_module):
    with patch(f"{currency_module.__name__}.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"rates": {"USD": 1.0}}  # EUR missing
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        args = {"from_currency": "USD", "to_currency": "EUR", "amount": 100}
        # The function wraps ValueError as "Invalid input: <message>"
        with pytest.raises(ValueError, match=r"Invalid input: Invalid currency code: EUR"):
            currency_module.convert_currency(args)


# --------- Network / API errors ---------
def test_api_request_exception_maps_to_connection_error(currency_module):
    with patch(f"{currency_module.__name__}.requests.get") as mock_get:
        mock_get.side_effect = requests.RequestException("boom")
        args = {"from_currency": "USD", "to_currency": "EUR", "amount": 100}
        with pytest.raises(ConnectionError, match=r"Failed to fetch exchange rates: boom"):
            currency_module.convert_currency(args)

def test_unexpected_exception_maps_to_runtime_error(currency_module):
    with patch(f"{currency_module.__name__}.requests.get") as mock_get:
        mock_get.side_effect = Exception("Network down")
        args = {"from_currency": "USD", "to_currency": "EUR", "amount": 100}
        with pytest.raises(RuntimeError, match=r"Conversion error: Network down"):
            currency_module.convert_currency(args)
