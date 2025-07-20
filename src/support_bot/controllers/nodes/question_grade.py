from typing import Literal
from langgraph.graph import MessagesState
from pydantic import BaseModel, Field

from support_bot.services.llms import GRADER_MODEL


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


def grade_questions(
    state: MessagesState,
) -> Literal["agentic_rag", "out_of_context_path"]:
    """Determine whether the user question is related to Hotmart customer support."""
    question = state["messages"][0].content

    prompt = QUESTION_GRADE_PROMPT.format(question=question)
    response = GRADER_MODEL.with_structured_output(GradeQuestion).invoke(
        [{"role": "user", "content": prompt}]
    )
    score = response.binary_score

    return "agentic_rag" if score.lower() == "yes" else "out_of_context_path"
