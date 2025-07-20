
from support_bot.base_models import GraphState
from support_bot.services.llms import RESPONDE_MODEL
from support_bot.services.database import Database

REWRITE_PROMPT = (
    "Look at the input and try to reason about the underlying semantic intent / meaning.\n"
    "Here is the initial question:"
    "\n ------- \n"
    "{question}"
    "\n ------- \n"
    "Formulate an improved question:"
)

ALT_REWRITE_PROMPT = (
    "Look at the input and try to reason about the underlying semantic intent / meaning.\n"
    "Here is the initial question:"
    "{question}"
    "\n ------- \n"
    "Check the user revenue to customize the answer based on the context condition. "
    "R${user_revenue}"
    "\n ------- \n"
    "Formulate an improved question:"
)

# Mock Database
db = Database()


def rewrite_question(state: GraphState):
    """Rewrite the original user question."""
    print("generate_answer")
    messages = state["messages"]
    question = messages[0].content
    context = messages[-1].content
    user_revenue = db.get_user_revenue()

    if "Hotmart Journey" in context:
        prompt = ALT_REWRITE_PROMPT.format(
            question=question, context=context, user_revenue=user_revenue
        )
    else:
        prompt = REWRITE_PROMPT.format(question=question, context=context)

    response = RESPONDE_MODEL.invoke([{"role": "user", "content": prompt}])
    return {"messages": [{"role": "user", "content": response.content}]}
