from langgraph.graph import MessagesState


class GraphState(MessagesState):
    retrieved_context: str
    decision: str
