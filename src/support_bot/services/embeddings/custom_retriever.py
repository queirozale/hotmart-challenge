from typing import List
from pydantic import Field

from langchain.schema import Document
from langchain.vectorstores import VectorStore
from langchain_core.vectorstores import VectorStoreRetriever


class CustomRetriever(VectorStoreRetriever):
    def __init__(
        self,
        vectorstore: VectorStore,
        search_kwargs: dict = Field(default_factory=dict),
        **kwargs,
    ):
        super().__init__(vectorstore=vectorstore, **kwargs)
        self.vectorstore = vectorstore
        self.search_kwargs = search_kwargs

    def get_relevant_documents(self, query: str) -> List[Document]:
        results: List[Document] = self.vectorstore.similarity_search(
            query, k=self.search_kwargs["k"]
        )
        print(f"Retrieved {len(results)} documents for the query: {query}")

        documents: List[Document] = []
        for result in results:
            doc_context = result.metadata["article_content"]
            documents.append(Document(page_content=doc_context))

        return documents
