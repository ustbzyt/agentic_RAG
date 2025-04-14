from typing import Dict, Any, Optional
from smolagents import Tool
from huggingface_hub import list_models
import os
import requests
from dataclasses import dataclass

@dataclass
class WeatherData:
    """Data class for weather information."""
    main_weather: str
    description: str
    temp: float
    feels_like: float
    humidity: int
    wind_speed: float
    city_name: str

class WeatherInfoTool(Tool):
    name = "weather_info"
    description = "Fetches real-time weather information for a given location using OpenWeatherMap API."
    inputs = {
        "location": {
            "type": "string",
            "description": "The city name (and optional country code, e.g., 'London,UK') to get weather information for."
        }
    }
    output_type = "string"

    def __init__(self) -> None:
        """Initialize the weather tool with API key."""
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not self.api_key:
            print("Warning: OPENWEATHERMAP_API_KEY environment variable not set. Weather tool will not function.")
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.is_initialized = True

    def _parse_weather_data(self, data: Dict[str, Any]) -> WeatherData:
        """Parse weather data from API response."""
        return WeatherData(
            main_weather=data.get('weather', [{}])[0].get('main', 'N/A'),
            description=data.get('weather', [{}])[0].get('description', 'N/A'),
            temp=data.get('main', {}).get('temp', 'N/A'),
            feels_like=data.get('main', {}).get('feels_like', 'N/A'),
            humidity=data.get('main', {}).get('humidity', 'N/A'),
            wind_speed=data.get('wind', {}).get('speed', 'N/A'),
            city_name=data.get('name', 'Unknown')
        )

    def _format_weather_output(self, weather: WeatherData) -> str:
        """Format weather data into a readable string."""
        return (
            f"Weather in {weather.city_name}:\n"
            f"- Condition: {weather.main_weather} ({weather.description})\n"
            f"- Temperature: {weather.temp}°C (Feels like: {weather.feels_like}°C)\n"
            f"- Humidity: {weather.humidity}%\n"
            f"- Wind Speed: {weather.wind_speed} m/s"
        )

    def forward(self, location: str) -> str:
        """Fetch and return weather information for the given location."""
        if not self.api_key:
            return "Error: Weather API key not configured."

        params = {
            'q': location,
            'appid': self.api_key,
            'units': 'metric'
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("cod") != 200:
                error_message = data.get("message", "Unknown API error")
                return f"Error fetching weather for '{location}': {error_message}"

            weather = self._parse_weather_data(data)
            return self._format_weather_output(weather)

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 401:
                return f"Error fetching weather for '{location}': Invalid API key or subscription issue."
            elif response.status_code == 404:
                return f"Error fetching weather: Location '{location}' not found."
            return f"HTTP error occurred while fetching weather for '{location}': {http_err}"
        except requests.exceptions.RequestException as req_err:
            return f"Error connecting to weather service for '{location}': {req_err}"
        except Exception as e:
            return f"An unexpected error occurred while fetching weather for '{location}': {e}"

class HubStatsTool(Tool):
    name = "hub_stats"
    description = (
        "Fetches the most downloaded model from a specific author or organization on the Hugging Face Hub. "
        "Use this tool when you need to find popular models from a known entity like 'google', 'facebook', 'microsoft', 'openai', etc. "
        "Requires the exact Hugging Face username or organization ID."
    )
    inputs = {
        "author": {
            "type": "string",
            "description": (
                "The exact Hugging Face username or organization ID (e.g., 'google', 'facebook', 'microsoft'). "
                "Do NOT provide company names like 'Meta' if their Hugging Face ID is different (e.g., use 'facebook' for Meta AI)."
            )
        }
    }

    def forward(self, author: str) -> str:
        """Fetch and return the most downloaded model for the given author."""
        try:
            models = list(list_models(author=author, sort="downloads", direction=-1, limit=1))
            
            if not models:
                return f"No models found for author {author}."
            
            model = models[0]
            return f"The most downloaded model by {author} is {model.id} with {model.downloads:,} downloads."
            
        except Exception as e:
            return f"Error fetching models for {author}: {str(e)}"

