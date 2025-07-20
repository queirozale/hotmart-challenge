from support_bot.base_models import GraphState
from support_bot.services.llms import RESPONDE_MODEL
from support_bot.services.database import Database

GENERATE_PROMPT = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer the question. "
    "If you don't know the answer, just say that you don't know. "
    "Use three sentences maximum and keep the answer concise.\n"
    "Question: {question} \n"
    "Context: {context}"
)

ALT_GENERATE_PROMPT = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer the question. "
    "Check the user revenue to customize the answer based on the context condition. "
    "Use three sentences maximum and keep the answer concise.\n"
    "Question: {question} \n"
    "Context: {context} \n"
    "User Revenue R${user_revenue} "
)

# Mock Database
db = Database()


def generate_answer(state: GraphState):
    """Generate an answer."""
    print("generate_answer")
    question = state["messages"][0].content
    context = state["messages"][-1].content
    user_revenue = db.get_user_revenue()

    if "Hotmart Journey" in context:
        prompt = ALT_GENERATE_PROMPT.format(
            question=question, context=context, user_revenue=user_revenue
        )
    else:
        prompt = GENERATE_PROMPT.format(question=question, context=context)

    response = RESPONDE_MODEL.invoke([{"role": "user", "content": prompt}])
    return {"messages": [response]}
