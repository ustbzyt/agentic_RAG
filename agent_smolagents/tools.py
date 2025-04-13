from smolagents import Tool
from huggingface_hub import list_models
import os
import requests


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

    def __init__(self):
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not self.api_key:
            print("Warning: OPENWEATHERMAP_API_KEY environment variable not set. Weather tool will not function.")
            # raise ValueError("OPENWEATHERMAP_API_KEY environment variable not set.")
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        self.is_initialized = True
        print("WeatherInfoTool initialized.") # Optional: Add a print statement for confirmation


    def forward(self, location: str):
        # Set up parameters for the API request
        params = {
            'q': location,          # The location query
            'appid': self.api_key,  # Your API key
            'units': 'metric'       # Request temperature in Celsius
        }

        try:
            # Make the GET request to the OpenWeatherMap API
            response = requests.get(self.base_url, params=params)
            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status()

            # Parse the JSON response
            data = response.json()

            # Check the response code within the JSON data (OpenWeatherMap specific)
            if data.get("cod") != 200:
                 # Extract the error message provided by the API
                 error_message = data.get("message", "Unknown API error")
                 return f"Error fetching weather for '{location}': {error_message}"

            # Extract relevant weather information
            main_weather = data.get('weather', [{}])[0].get('main', 'N/A')
            description = data.get('weather', [{}])[0].get('description', 'N/A')
            temp = data.get('main', {}).get('temp', 'N/A')
            feels_like = data.get('main', {}).get('feels_like', 'N/A')
            humidity = data.get('main', {}).get('humidity', 'N/A')
            wind_speed = data.get('wind', {}).get('speed', 'N/A')
            city_name = data.get('name', location) # Use the name returned by API for confirmation

            # Format the output string
            return (
                f"Weather in {city_name}:\n"
                f"- Condition: {main_weather} ({description})\n"
                f"- Temperature: {temp}°C (Feels like: {feels_like}°C)\n"
                f"- Humidity: {humidity}%\n"
                f"- Wind Speed: {wind_speed} m/s"
            )
        except requests.exceptions.HTTPError as http_err:
            # Handle HTTP errors (like 401 Unauthorized, 404 Not Found)
            if response.status_code == 401:
                return f"Error fetching weather for '{location}': Invalid API key or subscription issue."
            elif response.status_code == 404:
                 return f"Error fetching weather: Location '{location}' not found."
            else:
                return f"HTTP error occurred while fetching weather for '{location}': {http_err}"
        except requests.exceptions.RequestException as req_err:
            # Handle other network-related errors (connection, timeout, etc.)
            return f"Error connecting to weather service for '{location}': {req_err}"
        except Exception as e:
            # Catch any other unexpected errors (e.g., JSON parsing issues)
            return f"An unexpected error occurred while fetching weather for '{location}': {e}"


class HubStatsTool(Tool):
    name = "hub_stats"
    description = "Fetches the most downloaded model from a specific author on the Hugging Face Hub."
    inputs = {
        "author": {
            "type": "string",
            "description": "The username of the model author/organization to find models from."
        }
    }
    output_type = "string"

    def forward(self, author: str):
        try:
            # List models from the specified author, sorted by downloads
            models = list(list_models(author=author, sort="downloads", direction=-1, limit=1))
            
            if models:
                model = models[0]
                return f"The most downloaded model by {author} is {model.id} with {model.downloads:,} downloads."
            else:
                return f"No models found for author {author}."
        except Exception as e:
            return f"Error fetching models for {author}: {str(e)}"

