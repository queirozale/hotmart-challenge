import uuid
from pydantic import BaseModel, Field
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END

from support_bot.controllers.subgraphs.agentic_rag import SUBGRAPH
from support_bot.controllers.nodes.human_approval import (
    human_approval,
    approved_node,
    rejected_node,
)
from support_bot.controllers.nodes.out_of_context import out_of_context_node
from support_bot.controllers.nodes.question_grade import grade_questions
from support_bot.controllers.nodes.supervisor import supervisor_node

QUESTION_GRADE_PROMPT = (
    "You are a grader assessing if a question is related with Hotmart customer support. \n "
    "Here is the user question: {question} \n"
    "If the question contains keyword(s) or semantic meaning related to Hotmart, grade it as related. \n"
    "Give a binary score 'yes' or 'no' score to indicate whether the question is related with Hotmart or not."
)


class GradeQuestion(BaseModel):
    """Grade questions using a binary score for customer support related check."""

    binary_score: str = Field(
        description="Relevance score: 'yes' if related, or 'no' if not related"
    )


def call_subgraph(state: MessagesState):
    config = {"configurable": {"thread_id": uuid.uuid4()}}
    response = SUBGRAPH.invoke({"messages": state["messages"]}, config=config)
    return {"messages": response["messages"]}


from langgraph.graph.state import StateGraph, START


workflow = StateGraph(MessagesState)
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("agentic_rag", call_subgraph)
workflow.add_node("out_of_context_path", out_of_context_node)
workflow.add_node(human_approval)
workflow.add_node("approved_path", approved_node)
workflow.add_node("rejected_path", rejected_node)


workflow.add_edge(START, "supervisor")
workflow.add_conditional_edges(
    "supervisor",
    # Assess agent decision
    grade_questions,
)
workflow.add_edge("agentic_rag", "human_approval")
workflow.add_edge("approved_path", END)
workflow.add_edge("rejected_path", END)
workflow.add_edge("out_of_context_path", END)


GRAPH = workflow.compile()
