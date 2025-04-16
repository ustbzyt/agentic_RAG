from .agent_core import react_graph
from langchain_core.messages import HumanMessage, AIMessage
from .langfuse_client import langfuse_handler  # Optional
import os
from .agent_state import AgentState

# Initialize state
state: AgentState = {"messages": []}



def main():
    """Runs the interactive command-line interface for the agent."""
    print("Welcome to the Alfred Agent! Type 'quit' or 'exit' to end the conversation.")

    # Initialize state for the conversation
    # The state will be updated after each graph invocation
    conversation_state: AgentState = {"messages": []}

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["quit", "exit"]:
                print("Alfred: Goodbye, sir.")
                break
            current_messages = conversation_state.get("messages", [])
            current_messages.append(HumanMessage(content=user_input))
            graph_input: AgentState = {"messages": current_messages}
            result = react_graph.invoke(
                input=graph_input,
                config={
                    "callbacks": [langfuse_handler],
                    "metadata": {"mode": "interactive"}
                }
            )
            conversation_state = result
            if conversation_state and "messages" in conversation_state and conversation_state["messages"]:
                last_message = conversation_state["messages"][-1]
                # Ensure we're printing an AI response, not the user's input again
                if isinstance(last_message, AIMessage):
                    print(f"Alfred: {last_message.content}")
                # Handle cases where the last message might be a tool call result (less common here)
                # or if the graph somehow ends without a final AIMessage.
                elif hasattr(last_message, 'content'):
                     print(f"Alfred: {last_message.content}") # Print content if available
                else:
                     print("Alfred: (Received a non-standard final message)")

            else:
                print("Alfred: (No response generated)") # Should not happen in normal flow

        except KeyboardInterrupt:
            print("\nAlfred: Interrupt received. Goodbye, sir.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()