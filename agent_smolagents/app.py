import gradio as gr
from smolagents import GradioUI, CodeAgent, DuckDuckGoSearchTool, LiteLLMModel
import os # Import the os module to access environment variables
from dotenv import load_dotenv # Optional: Load .env file if you use one

# Import our custom tools from their modules
from agent_smolagents.tools import WeatherInfoTool, HubStatsTool
from agent_smolagents.retriever import load_guest_dataset

# --- Import tracing functions and state ---
# Import initialize function, the decorator, and the enabled flag
from agent_smolagents.tracing import initialize_otel_tracing, traced_handler, IS_TRACING_ENABLED as TRACING_ENABLED_FLAG

# Call the initialization function early in the script execution
initialize_otel_tracing() # This now sets the IS_TRACING_ENABLED flag in tracing.py
# --- End OTel tracing setup ---

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


# --- Agent Initialization ---
# Agent operations will be automatically traced if IS_TRACING_ENABLED is True
alfred = CodeAgent(
    tools=[guest_info_tool, weather_info_tool, hub_stats_tool, search_tool],
    model=model,
    add_base_tools=True,
    planning_interval=3
)

# --- Apply the tracing decorator (imported from tracing.py) ---
# Use the flag imported from tracing.py
if TRACING_ENABLED_FLAG:
    if hasattr(alfred, 'run') and callable(alfred.run):
         print("Applying tracing decorator to alfred.run")
         alfred.run = traced_handler(alfred.run) # Use the imported decorator
    else:
         print("Warning: Could not find 'run' method on agent instance to apply tracing decorator.")
# --- End Decorator Application ---

if __name__ == "__main__":
    print("Launching Gradio UI with Gemini model via LiteLLM...")
    # Use the flag imported from tracing.py
    if TRACING_ENABLED_FLAG:
        print("Langfuse OpenTelemetry tracing is active.")
    else:
        print("Langfuse OpenTelemetry tracing is disabled.")

    GradioUI(alfred).launch()
