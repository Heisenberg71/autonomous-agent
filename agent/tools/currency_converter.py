import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()
API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
if not API_KEY:
    raise ValueError("EXCHANGE_RATE_API_KEY not found in environment variables")

BASE_URL = "https://api.exchangerate-api.com/v4/latest"

def convert_currency(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert amount from one currency to another.
    
    Args:
        args (dict): Dictionary containing:
            - from_currency (str): Source currency code (e.g., 'USD')
            - to_currency (str): Target currency code (e.g., 'EUR')
            - amount (float): Amount to convert
    
    Returns:
        dict: Conversion result with format:
            {
                "from": "USD",
                "to": "EUR",
                "amount": 100,
                "result": 92.14,
                "rate": 0.9214
            }
    
    Raises:
        ValueError: If invalid currency codes or amount
        ConnectionError: If API request fails
    """
    try:
        # Extract parameters
        from_currency = args.get('from_currency', '').upper()
        to_currency = args.get('to_currency', '').upper()
        amount = float(args.get('amount', 0))

        # Validate inputs
        if not all([from_currency, to_currency, amount]):
            raise ValueError("Missing required parameters")
        
        if amount < 0:
            raise ValueError("Amount must be positive")

        # Make API request
        response = requests.get(f"{BASE_URL}/{from_currency}")
        response.raise_for_status()
        
        rates = response.json()['rates']
        if to_currency not in rates:
            raise ValueError(f"Invalid currency code: {to_currency}")

        # Calculate conversion
        rate = rates[to_currency]
        result = amount * rate

        return {
            "from": from_currency,
            "to": to_currency,
            "amount": amount,
            "result": round(result, 2),
            "rate": rate
        }

    except requests.RequestException as e:
        raise ConnectionError(f"Failed to fetch exchange rates: {str(e)}")
    except (ValueError, KeyError) as e:
        raise ValueError(f"Invalid input: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Conversion error: {str(e)}")