from langchain_core.tools import tool
from dataclasses import dataclass
import requests
import os
from typing import Dict, Any, List
from .retriever import guest_info_retriever

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import Runnable


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

@tool
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

tools: List[Any] = [guest_info_retriever, get_weather_info]

try:
    # 1. Ensure GEMINI_API_KEY is set in your environment variables
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

    # 2. Initialize the Gemini LLM
    #    Choose the model you want to use, e.g., "gemini-1.5-flash", "gemini-pro"
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=gemini_api_key)

    # 3. Bind the tools to the LLM
    llm_with_tools = llm.bind_tools(tools)

    # 4. This is your agent_runnable
    agent_runnable: Runnable = llm_with_tools

except Exception as e:
    # Provide a more informative error message if initialization fails
    print(f"Error initializing Gemini model or binding tools: {e}")
    # Depending on your application's needs, you might want to exit or raise the error
    raise RuntimeError(f"Failed to create Gemini agent runnable: {e}") from e
