from langchain.tools.retriever import create_retriever_tool

from support_bot.services.embeddings.custom_retriever import CustomRetriever
from support_bot.services.embeddings.vector_store import VECTORSTORE

retriever = CustomRetriever(vectorstore=VECTORSTORE, search_kwargs={"k": 1})
retriever_tool = create_retriever_tool(
    retriever,
    "retrieve_faq_articles",
    "Search and return FAQ articles about Hotmart.",
)
