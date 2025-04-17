import os
import logging
from typing import List
from smolagents import Tool, GradioUI, CodeAgent, DuckDuckGoSearchTool, LiteLLMModel
from dotenv import load_dotenv

# Import custom tools and utilities
from .tools import WeatherInfoTool, HubStatsTool
from .retriever import load_guest_dataset
from .tracing import (
    initialize_otel_tracing,
    traced_handler,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def initialize_model() -> LiteLLMModel:
    """Initialize and return the Gemini model instance."""
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

    logger.info("Initializing Gemini model...")
    return LiteLLMModel(
        model_id="gemini/gemini-2.0-flash",
        api_key=gemini_api_key,
    )

def initialize_tools() -> List[Tool]:
    """Initialize and return a list of all available tools."""
    logger.info("Initializing tools...")
    return [
        load_guest_dataset(),  # Guest info retriever
        WeatherInfoTool(),     # Weather information
        HubStatsTool(),        # Hugging Face Hub stats
        DuckDuckGoSearchTool() # Web search
    ]

def setup_tracing(agent: CodeAgent, tracing_enabled: bool) -> None:
    """Apply tracing decorator to the agent if tracing is enabled."""
    if tracing_enabled and hasattr(agent, 'run') and callable(agent.run):
        logger.info("Applying tracing decorator to agent.run")
        agent.run = traced_handler(agent.run)
    elif tracing_enabled:
        logger.warning("Could not find 'run' method on agent instance to apply tracing decorator.")

def main() -> None:
    """Main entry point for the application."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Initialize tracing
        tracing_initialized = initialize_otel_tracing()
        logger.info(f"Langfuse OpenTelemetry tracing is {'active' if tracing_initialized else 'disabled'}")
        
        # Initialize model and tools
        model = initialize_model()
        tools = initialize_tools()
        
        # Create and configure agent
        logger.info("Creating Alfred agent...")
        alfred = CodeAgent(
            tools=tools,
            model=model,
            add_base_tools=True,
            planning_interval=3
        )
        
        # Setup tracing if enabled
        setup_tracing(alfred, tracing_initialized)
        
        # Launch Gradio UI
        logger.info("Launching Gradio UI...")
        GradioUI(alfred).launch()
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
