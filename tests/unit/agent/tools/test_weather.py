import unittest
from unittest.mock import patch, Mock
import os
import sys
import requests
from dotenv import load_dotenv

# Add src/ to sys.path so imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../src")))

from agent.tools.weather import get_weather_details, API_KEY, DATE, MAX_TEMPERATURE_IN_CELCIOUS, MIN_TEMPERATURE_IN_CELCIOUS, AVERAGE_TEMPERATURE_IN_CELCIOUS, WEATHER_CONDITION

class TestWeatherAPI(unittest.TestCase):
    def setUp(self):
        # Load environment variables
        load_dotenv()
        self.api_key = os.getenv('WEATHER_API_KEY')
        if not self.api_key:
            self.skipTest("WEATHER_API_KEY not found in environment variables")
        
        # Sample valid input
        self.valid_args = {
            'city': 'London',
            'from_date': '2023-01-01',
            'to_date': '2023-01-02'
        }
        
        # Mock API response
        self.mock_response = {
            'forecast': {
                'forecastday': [
                    {
                        'date': '2023-01-01',
                        'day': {
                            'maxtemp_c': 15.5,
                            'mintemp_c': 5.0,
                            'avgtemp_c': 10.2,
                            'condition': {'text': 'Sunny'}
                        }
                    },
                    {
                        'date': '2023-01-02',
                        'day': {
                            'maxtemp_c': 14.0,
                            'mintemp_c': 4.5,
                            'avgtemp_c': 9.8,
                            'condition': {'text': 'Partly cloudy'}
                        }
                    }
                ]
            }
        }

    @patch('agent.tools.weather.requests.get')
    def test_successful_weather_fetch(self, mock_get):
        # Arrange
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = self.mock_response
        
        # Act
        result = get_weather_details(self.valid_args)
        
        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][DATE], '2023-01-01')
        self.assertEqual(result[0][MAX_TEMPERATURE_IN_CELCIOUS], 15.5)
        self.assertEqual(result[0][MIN_TEMPERATURE_IN_CELCIOUS], 5.0)
        self.assertEqual(result[0][AVERAGE_TEMPERATURE_IN_CELCIOUS], 10.2)
        self.assertEqual(result[0][WEATHER_CONDITION], 'Sunny')
        mock_get.assert_called_once()

    @patch('agent.tools.weather.requests.get')
    def test_missing_city(self, mock_get):
        # Arrange
        args = self.valid_args.copy()
        args.pop('city')
        
        # Act
        result = get_weather_details(args)
        
        # Assert
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith("Error from system: Missing required parameters"))
        mock_get.assert_not_called()

    @patch('agent.tools.weather.requests.get')
    def test_missing_from_date(self, mock_get):
        # Arrange
        args = self.valid_args.copy()
        args.pop('from_date')
        
        # Act
        result = get_weather_details(args)
        
        # Assert
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith("Error from system: Missing required parameters"))
        mock_get.assert_not_called()

    @patch('agent.tools.weather.requests.get')
    def test_missing_to_date(self, mock_get):
        # Arrange
        args = self.valid_args.copy()
        args.pop('to_date')
        
        # Act
        result = get_weather_details(args)
        
        # Assert
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith("Error from system: Missing required parameters"))
        mock_get.assert_not_called()

    @patch('agent.tools.weather.requests.get')
    def test_invalid_date_format(self, mock_get):
        # Arrange
        args = self.valid_args.copy()
        args['from_date'] = 'invalid-date'
        
        # Act
        result = get_weather_details(args)
        
        # Assert
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith("Error from system: Invalid isoformat string"))
        mock_get.assert_not_called()

    @patch('agent.tools.weather.requests.get')
    def test_api_connection_error(self, mock_get):
        # Arrange
        mock_get.side_effect = requests.RequestException("Connection error")
        
        # Act/Assert
        with self.assertRaises(ConnectionError) as cm:
            get_weather_details(self.valid_args)
        self.assertTrue(str(cm.exception).startswith("Failed to fetch weather detail: Connection error"))

    @patch('agent.tools.weather.requests.get')
    def test_api_no_forecast_data(self, mock_get):
        # Arrange
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = {'error': 'No forecast data'}
        
        # Act
        result = get_weather_details(self.valid_args)
        
        # Assert
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith("Error from system: No forecast data in response"))
        mock_get.assert_called_once()

    @patch('agent.tools.weather.requests.get')
    def test_api_bad_status_code(self, mock_get):
        # Arrange
        mock_get.return_value = Mock(status_code=404)
        mock_get.return_value.raise_for_status.side_effect = requests.HTTPError("404 Client Error")
        
        # Act/Assert
        with self.assertRaises(ConnectionError) as cm:
            get_weather_details(self.valid_args)
        self.assertTrue(str(cm.exception).startswith("Failed to fetch weather detail: 404 Client Error"))