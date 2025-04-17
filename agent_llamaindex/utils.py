from llama_index.tools.duckduckgo import DuckDuckGoSearchToolSpec
from llama_index.core.tools import FunctionTool
import os
import requests
from dataclasses import dataclass
from typing import Dict, Any
import logging 
from .retriever import guest_info_retriever

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# Initialize the DuckDuckGo search tool
try:
    logger.info("Initializing DuckDuckGo Search Tool...")
    # Initialize the spec first
    duckduckgo_spec = DuckDuckGoSearchToolSpec()
    # Wrap the specific search method into a FunctionTool
    search_tool = FunctionTool.from_defaults(
        fn=duckduckgo_spec.duckduckgo_full_search, # The actual function to call
        name="duckduckgo_search", # Name for the agent to identify the tool
        description=( # Description for the agent to understand when to use it
            "A tool that performs a web search using DuckDuckGo to find information "
            "on recent events, specific topics, or anything not in the local knowledge base."
        )
    )
    logger.info("DuckDuckGo Search Tool initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing DuckDuckGo Search Tool: {e}", exc_info=True)
    search_tool = None # Indicate failure
# Example usage
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

def _parse_weather_data(data: Dict[str, Any]) -> WeatherData:
    """Parse weather data from API response."""
    # Safely access nested dictionary keys
    weather_info = data.get('weather', [{}])[0]
    main_info = data.get('main', {})
    wind_info = data.get('wind', {})

    return WeatherData(
        main_weather=weather_info.get('main', 'N/A'),
        description=weather_info.get('description', 'N/A'),
        temp=main_info.get('temp'), # Let potential errors propagate if temp is crucial
        feels_like=main_info.get('feels_like'),
        humidity=main_info.get('humidity'),
        wind_speed=wind_info.get('speed'),
        city_name=data.get('name', 'Unknown')
    )

def _format_weather_output(weather: WeatherData) -> str:
    """Format weather data into a readable string."""
    # Handle potential None values if parsing failed or data was missing
    temp_str = f"{weather.temp}°C" if weather.temp is not None else "N/A"
    feels_like_str = f"{weather.feels_like}°C" if weather.feels_like is not None else "N/A"
    humidity_str = f"{weather.humidity}%" if weather.humidity is not None else "N/A"
    wind_speed_str = f"{weather.wind_speed} m/s" if weather.wind_speed is not None else "N/A"

    return (
        f"Weather in {weather.city_name}:\n"
        f"- Condition: {weather.main_weather} ({weather.description})\n"
        f"- Temperature: {temp_str} (Feels like: {feels_like_str})\n"
        f"- Humidity: {humidity_str}\n"
        f"- Wind Speed: {wind_speed_str}"
    )

def get_weather_info(location: str) -> str:
    """Fetches real-time weather information for a given location using OpenWeatherMap API."""
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        # Consider logging a warning instead of printing to stdout in production
        print("Warning: OPENWEATHERMAP_API_KEY environment variable not set. Weather tool will not function.")
        return "Error: Weather API key not configured."

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': location,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        # Check API-specific error code
        if data.get("cod") != 200:
            error_message = data.get("message", "Unknown API error")
            return f"Error fetching weather for '{location}': {error_message}"

        weather = _parse_weather_data(data)
        return _format_weather_output(weather)

    except requests.exceptions.HTTPError as http_err:
        # More specific error handling based on status code
        status_code = http_err.response.status_code
        if status_code == 401:
            return f"Error fetching weather for '{location}': Invalid API key or subscription issue."
        elif status_code == 404:
            return f"Error fetching weather: Location '{location}' not found."
        else:
            return f"HTTP error occurred while fetching weather for '{location}': {http_err}"
    except requests.exceptions.RequestException as req_err:
        # Handle connection errors, timeouts, etc.
        return f"Error connecting to weather service for '{location}': {req_err}"
    except Exception as e:
        # Catch unexpected errors during parsing or formatting
        # Consider logging the full exception details
        print(f"An unexpected error occurred: {e}") # Log this properly
        return f"An unexpected error occurred while processing weather for '{location}'."

# Wrap the weather function into a FunctionTool
try:
    logger.info("Initializing Weather Info Tool...")
    weather_tool = FunctionTool.from_defaults(
        fn=get_weather_info,
        name="get_weather_information", # Descriptive name
        description=( # Clear description for the agent
            "Provides the current weather conditions (temperature, condition, humidity, wind speed) "
            "for a specified city. Use this tool when asked about the weather in a particular location."
            "Input should be the city name (e.g., 'London', 'Tokyo')."
        )
    )
    logger.info("Weather Info Tool initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing Weather Info Tool: {e}", exc_info=True)
    weather_tool = None # Indicate failure

tools = [tool for tool in [search_tool, weather_tool, guest_info_retriever] if tool is not None]
