from langgraph.graph import MessagesState


def out_of_context_node(state: MessagesState) -> MessagesState:
    print("❌ Apenas posso responder a perguntas referentes à Hotmart")
    return state
