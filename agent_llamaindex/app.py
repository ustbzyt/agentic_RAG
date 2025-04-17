from llama_index.core.agent import ReActAgent
from llama_index.llms.google_genai import GoogleGenAI

import os
import asyncio
import logging
from dotenv import load_dotenv
from .utils import tools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def initialize_agent():
    """Initialize the Gemini model and create the Alfred agent."""
    # Load environment variables
    load_dotenv()
    
    # Check for required API key
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        logger.error("FATAL: GEMINI_API_KEY environment variable not set!")
        exit("API Key not configured. Please set the GEMINI_API_KEY environment variable.")
    
    logger.info("Initializing Gemini model...")
    llm = GoogleGenAI(
        model_name="models/gemini-1.5-flash",
        api_key=GEMINI_API_KEY
    )
    
    # Create Alfred agent with tools
    logger.info("Creating Alfred agent...")
    return ReActAgent.from_tools(
        tools=tools,
        llm=llm,
        verbose=True
    )

async def main():
    """Run the conversational loop for the Alfred agent."""
    # Initialize agent
    alfred = initialize_agent()
    
    # Welcome message
    print("\n🎩 Alfred is ready to assist. Ask about guests, weather, or search the web.")
    print("   Type 'quit' or 'exit' to end the conversation.")
    print("-" * 30)

    while True:
        try:
            # Get user input
            user_query = input("You: ").strip()
            
            # Handle exit commands
            if user_query.lower() in ['quit', 'exit']:
                print("\n🎩 Alfred bids you farewell!")
                break
                
            # Skip empty input
            if not user_query:
                continue

            # Process query
            logger.info(f"Processing query: \"{user_query}\"")
            response = await alfred.achat(user_query)

            # Display response
            print("\n🎩 Alfred:")
            print(response)
            print("-" * 30)

        except EOFError:  # Handle Ctrl+D
            print("\n🎩 Alfred bids you farewell!")
            break
        except KeyboardInterrupt:  # Handle Ctrl+C
            print("\n🎩 Alfred bids you farewell!")
            break
        except Exception as e:
            logger.error(f"Error during agent execution: {e}", exc_info=True)
            print(f"\n💥 Alfred encountered an error: {e}")
            print("-" * 30)

if __name__ == "__main__":
    asyncio.run(main())