from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    """Shared state that flows through every node in the graph."""
    messages: Annotated[list, add_messages]