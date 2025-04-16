from langchain_core.messages import SystemMessage
from .agent_state import AgentState
from .utils import agent_runnable
from langchain_core.runnables import Runnable

def assistant(state: AgentState) -> AgentState:
    """Let LangGraph handle tool use; return model output directly."""

    # If no previous messages, initialize with system prompt
    if not state['messages']:
        textual_description_of_tools = """
        get_weather_info(location: str) -> str:
        Fetches real-time weather information for a given location using OpenWeatherMap API.
        retrieve_guest_info(query: str) -> str:
        Retrieves detailed information about gala guests based on their name or relation.
        """
        sys_prompt = f"""
        You are a helpful butler named Alfred serving Mr. Wayne and Batman.
        You can use the tools below:
        {textual_description_of_tools}
        """

        state["messages"] = [SystemMessage(content=sys_prompt)]

    # Run the model (which may call tools)
    result = agent_runnable.invoke(state["messages"])

    # Append the result to the message history
    state["messages"].append(result)
    return state