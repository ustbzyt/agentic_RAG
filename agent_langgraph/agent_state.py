from typing import TypedDict, List, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    Represents the state of the agent during conversation.
    
    Attributes:
        messages: List of messages in the conversation history
    """
    messages: Annotated[List[AnyMessage], add_messages]