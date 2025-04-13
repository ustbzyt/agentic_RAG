import gradio as gr
from smolagents import GradioUI, CodeAgent, LiteLLMModel
import os # Import the os module to access environment variables
from dotenv import load_dotenv # Optional: Load .env file if you use one


# Import our custom tools from their modules
from agent_smolagents.tools import DuckDuckGoSearchTool, WeatherInfoTool, HubStatsTool
from agent_smolagents.retriever import load_guest_dataset

# Optional: Load environment variables from a .env file
load_dotenv()

# --- Model Initialization Change ---
# Initialize the Google Gemini model
# Make sure GEMINI_API_KEY environment variable is set
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

# Initialize using LiteLLMModel
# Use a valid model name prefixed with 'gemini/'
# e.g., "gemini/gemini-pro", "gemini/gemini-1.5-flash", "gemini/gemini-1.5-pro"
model = LiteLLMModel(
    model_id="gemini/gemini-1.5-flash", # Adjust model name as needed
    api_key=gemini_api_key,
    # max_tokens=8192 # Optional
)
# --- End Model Initialization Change ---

# Initialize the web search tool
search_tool = DuckDuckGoSearchTool()

# Initialize the weather tool
weather_info_tool = WeatherInfoTool()

# Initialize the Hub stats tool
hub_stats_tool = HubStatsTool()

# Load the guest dataset and initialize the guest info tool
# This now correctly calls the function in retriever.py
guest_info_tool = load_guest_dataset()


# Create Alfred with all the tools
alfred = CodeAgent(
    tools=[guest_info_tool, weather_info_tool, hub_stats_tool, search_tool], 
    model=model,
    add_base_tools=True,  # Add any additional base tools
    planning_interval=3   # Enable planning every 3 steps
)

if __name__ == "__main__":
    # The check for the API key happens earlier now
    print("Launching Gradio UI with Gemini model via LiteLLM...")
    GradioUI(alfred).launch()