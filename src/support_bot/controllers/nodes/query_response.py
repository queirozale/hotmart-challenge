

from support_bot.base_models import GraphState
from support_bot.services.llms import RESPONDE_MODEL
from support_bot.services.tools.retriever_tool import retriever_tool


def generate_query_or_respond(state: GraphState):
    """Call the model to generate a response based on the current state. Given
    the question, it will decide to retrieve using the retriever tool, or simply respond to the user.
    """
    response = RESPONDE_MODEL.bind_tools([retriever_tool]).invoke(state["messages"])
    return {"messages": [response]}
