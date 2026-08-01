from src.componants.state.state import State


class BasicChatbotNode:
    """A single-node graph: user message in, LLM reply out."""

    def __init__(self, model):
        self.llm = model

    def process(self, state: State) -> dict:
        return {"messages": [self.llm.invoke(state["messages"])]}
