import unittest
from unittest.mock import patch, MagicMock
from weather_app import get_weather
import requests

class TestGetWeather(unittest.TestCase):

    @patch("weather_app.requests.get")
    def test_valid_city(self, mock_get):
        mock_get.side_effect = [
            MagicMock(json=lambda: {
                "results": [{"latitude": 40.85, "longitude": 14.27,
                             "name": "Naples", "country": "Italy"}]
            }),
            MagicMock(json=lambda: {
                "current": {"temperature_2m": 18.5,
                            "weather_code": 1,
                            "wind_speed_10m": 12.3}
            })
        ]
        result = get_weather("Napoli")
        self.assertEqual(result["source"], "api")
        self.assertIn("Naples", result["city"])

    @patch("weather_app.requests.get")
    def test_city_not_found(self, mock_get):
        mock_get.return_value = MagicMock(json=lambda: {})
        result = get_weather("CittàInesistente999")
        self.assertIn("error", result)

    def test_empty_input(self):
        result = get_weather("")
        self.assertEqual(result["error"],
                         "Il nome della città non può essere vuoto.")

    @patch("weather_app.requests.get",
           side_effect=requests.exceptions.ConnectionError)
    def test_network_error(self, mock_get):
        result = get_weather("Roma")
        self.assertIn("error", result)

    @patch("weather_app.requests.get",
           side_effect=requests.exceptions.Timeout)
    def test_timeout(self, mock_get):
        result = get_weather("Milano")
        self.assertIn("Scaduta", result["error"] or
                      "scaduta" in result["error"])

if __name__ == "__main__":
    unittest.main()
