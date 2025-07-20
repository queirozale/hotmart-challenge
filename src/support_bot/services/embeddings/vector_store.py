import os
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import logging
import logging.config

from support_bot.services.embeddings.doc_splitter import retrieve_splitted_docs
from support_bot.settings.base_settings import BaseAppSettings

logging.config.fileConfig("conf/logging.conf")
logger = logging.getLogger("hotmart-challenge")

base_settings = BaseAppSettings()
open_api_key = base_settings.open_api_key.get_secret_value()
os.environ["OPENAI_API_KEY"] = open_api_key

EMBEDDINGS_MODEL_VERSION = "text-embedding-3-large"


logger.info("Creating the vector store...")
split_docs = retrieve_splitted_docs()
embeddings = OpenAIEmbeddings(
    model=EMBEDDINGS_MODEL_VERSION,
)
VECTORSTORE = FAISS.from_documents(documents=split_docs, embedding=embeddings)
