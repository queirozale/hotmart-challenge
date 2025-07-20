from langgraph.graph import MessagesState


def supervisor_node(state: MessagesState) -> MessagesState:
    print("Just a dummy node")
    return state
