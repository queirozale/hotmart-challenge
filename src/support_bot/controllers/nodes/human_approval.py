from typing import Literal
from langgraph.types import interrupt, Command

from support_bot.base_models import GraphState


# Human approval node
def human_approval(
    state: GraphState,
) -> Command[Literal["approved_path", "rejected_path"]]:
    decision = interrupt(
        {"question": "Essa resposta foi útil?", "message": state["messages"][-1]}
    )

    if decision == "approve":
        return Command(goto="approved_path", update={"decision": "approved"})
    else:
        return Command(goto="rejected_path", update={"decision": "rejected"})


# Next steps after approval
def approved_node(state: GraphState) -> GraphState:
    print("✅ Usuário aprovou a resposta!")
    return state


# Alternative path after rejection
def rejected_node(state: GraphState) -> GraphState:
    print("❌ Procure um assistente")
    return state
