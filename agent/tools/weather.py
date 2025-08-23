import requests
import datetime
import os
from dotenv import load_dotenv

DATE = "date"
MAX_TEMPERATURE_IN_CELCIOUS = "max_tempareture_in_celcious"
MIN_TEMPERATURE_IN_CELCIOUS = "min_tempareture_in_celcious"
AVERAGE_TEMPERATURE_IN_CELCIOUS = "average_temperature_in_celcious"
WEATHER_CONDITION = "weather_condition"

# Load environment variables
load_dotenv()
API_KEY = os.getenv('WEATHER_API_KEY')
if not API_KEY:
    raise ValueError("WEATHER_API_KEY not found in environment variables")

BASE_URL = "http://api.weatherapi.com/v1"

def getWeather(args: dict):
    """
    Get weather data for a city between two dates.
    
    Args:
        args (dict): Dictionary containing:
            - city: Name of the city
            - from_date: Start date in ISO format
            - to_date: End date in ISO format
    
    Returns:
        list: Weather data for each day in the date range
    """
    # Extract parameters from args dictionary
    city = args.get('city')
    from_date = args.get('from_date')
    to_date = args.get('to_date')
    
    try:
        # Validate required parameters
        if not all([city, from_date, to_date]):
            raise ValueError("Missing required parameters: city, from_date, or to_date")

        # Convert dates to datetime objects
        start = datetime.date.fromisoformat(from_date)
        end = datetime.date.fromisoformat(to_date)

        weatherHistoryUrl = f"{BASE_URL}/history.json"
        params = {
            "key": API_KEY,
            "q": city,
            "dt": start.isoformat(),
            "end_dt": end.isoformat()
        }
        
        response = requests.get(weatherHistoryUrl, params=params)
        # Raise exception for bad status codes
        response.raise_for_status()

        data = response.json()
        # Check if we have forecast data
        if 'forecast' not in data:
            print(f"Debug - Full response: {data}")
            raise ValueError("No forecast data in response")

        # Collecting weather data for each day
        forecast_days = data['forecast']['forecastday']
        weatherHistory = []
        for day in forecast_days:
            day_info = {
                DATE: day['date'],
                MAX_TEMPERATURE_IN_CELCIOUS: day['day']['maxtemp_c'],
                MIN_TEMPERATURE_IN_CELCIOUS: day['day']['mintemp_c'],
                AVERAGE_TEMPERATURE_IN_CELCIOUS: day['day']['avgtemp_c'],
                WEATHER_CONDITION: day['day']['condition']['text']
            }
            weatherHistory.append(day_info)
        return weatherHistory

    except (ValueError) as e:
        return f"Error from system: {str(e)}"
    except Exception as e:
        return f"Weather Data Fetching Error: {str(e)}"