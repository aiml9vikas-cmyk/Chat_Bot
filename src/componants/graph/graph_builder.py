from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from src.componants.state.state import State
from src.componants.nodes.basic_chatbot_node import BasicChatbotNode
#from src.componants.nodes.chatbot_with_tool_node import ChatbotWithToolNode
#from src.componants.tools.search_tool import get_tools

class GraphBuilder:
    def __init__(self, model):
        self.llm=model
        self.graph_builder=StateGraph(State)

    def basic_chatbot_build_graph(self):
        self.graph_builder.add_node("chatbot",BasicChatbotNode(self.llm).process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)

    def setup_graph(self,usecase:str):
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        else:
            raise ValueError(f"Unknown usecase: {usecase}")

        return self.graph_builder.compile()