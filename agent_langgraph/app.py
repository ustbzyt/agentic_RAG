import logging
from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from .agent_core import react_graph
from .langfuse_client import langfuse_handler
from .agent_state import AgentState

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_response(conversation_state: AgentState) -> None:
    """Process and display the agent's response."""
    if not conversation_state or "messages" not in conversation_state:
        logger.warning("No response generated")
        print("Alfred: (No response generated)")
        return

    last_message = conversation_state["messages"][-1]
    if isinstance(last_message, AIMessage):
        print(f"Alfred: {last_message.content}")
    elif hasattr(last_message, 'content'):
        print(f"Alfred: {last_message.content}")
    else:
        logger.warning("Received non-standard message type")
        print("Alfred: (Received a non-standard final message)")

def main() -> None:
    """Run the interactive command-line interface for the agent."""
    try:
        print("\n🎩 Welcome to the Alfred Agent! Type 'quit' or 'exit' to end the conversation.")
        
        # Initialize conversation state
        conversation_state: AgentState = {"messages": []}
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                if user_input.lower() in ["quit", "exit"]:
                    print("\n🎩 Alfred: Goodbye, sir.")
                    break
                    
                # Update conversation state
                current_messages = conversation_state.get("messages", [])
                current_messages.append(HumanMessage(content=user_input))
                
                # Process input through the graph
                logger.info(f"Processing query: \"{user_input}\"")
                result = react_graph.invoke(
                    input={"messages": current_messages},
                    config={
                        "callbacks": [langfuse_handler],
                        "metadata": {"mode": "interactive"}
                    }
                )
                
                # Update state and display response
                conversation_state = result
                process_response(conversation_state)
                
            except KeyboardInterrupt:
                print("\n🎩 Alfred: Interrupt received. Goodbye, sir.")
                break
            except Exception as e:
                logger.error(f"Error processing input: {e}", exc_info=True)
                print(f"\n💥 Alfred encountered an error: {e}")
                
    except Exception as e:
        logger.error(f"Fatal error in main execution: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()