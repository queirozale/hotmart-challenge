from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import MessagesState

from support_bot.controllers.nodes.query_response import generate_query_or_respond
from support_bot.controllers.nodes.question_rewrite import rewrite_question
from support_bot.controllers.nodes.generate_answer import generate_answer
from support_bot.controllers.nodes.doc_grade import grade_documents
from support_bot.services.tools.retriever_tool import retriever_tool


checkpointer = InMemorySaver()

workflow = StateGraph(MessagesState)

# Define the nodes we will cycle between
workflow.add_node(generate_query_or_respond)
workflow.add_node("retrieve", ToolNode([retriever_tool]))
workflow.add_node(rewrite_question)
workflow.add_node(generate_answer)

workflow.add_edge(START, "generate_query_or_respond")

# Decide whether to retrieve
workflow.add_conditional_edges(
    "generate_query_or_respond",
    # Assess LLM decision (call `retriever_tool` tool or respond to the user)
    tools_condition,
    {
        # Translate the condition outputs to nodes in our graph
        "tools": "retrieve",
        END: END,
    },
)

# Edges taken after the `action` node is called.
workflow.add_conditional_edges(
    "retrieve",
    # Assess agent decision
    grade_documents,
)

workflow.add_edge("rewrite_question", "generate_query_or_respond")

# Compile
SUBGRAPH = workflow.compile(checkpointer=checkpointer)
