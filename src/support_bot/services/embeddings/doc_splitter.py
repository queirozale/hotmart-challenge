import re
import pandas as pd
from typing import List
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter


DATA_PATH = "data/articles.csv"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 20


def remove_html_tags(text: str) -> str:
    clean = re.compile("<.*?>")
    return re.sub(clean, "", text)


def retrieve_splitted_docs() -> List[Document]:
    df = pd.read_csv(DATA_PATH)
    df["docs"] = df.apply(
        lambda x: Document(
            page_content=x["article_name"],
            metadata={
                "article_url": x["article_url"],
                "article_content": remove_html_tags(x["article_content"].strip()),
            },
        ),
        axis=1,
    )

    lst_documents = df["docs"].tolist()
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    split_docs = text_splitter.split_documents(lst_documents)

    return split_docs
