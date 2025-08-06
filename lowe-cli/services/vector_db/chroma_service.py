from typing import List
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from services.huggingface.embedding_model_service import EmbeddingModelService
from utils.constants import Constants


class ChromaService:
    """Service to handle Chroma vector database operations."""
    
    def __init__(self) -> None:
        """Initialize the ChromaService with the specified embeddings model."""
        self.embeddings: HuggingFaceEmbeddings = EmbeddingModelService.get_huggingface_embeddings()

    def add(self, documents: List[Document]) -> None:
        """Add documents to the Chroma vector store."""
        vector_store: Chroma = self.__vector_store()
        vector_store.add_documents(documents=documents)

    def search(self, query: str, k: int = 5) -> List[Document]:
        """Search for similar documents in the Chroma vector store."""
        vector_store: Chroma = self.__vector_store()
        retrieved_docs: List[Document] = vector_store.similarity_search(query)
        return retrieved_docs

    def __vector_store(self) -> Chroma:
        """Get Chroma embeddings model."""
        vector_store: Chroma = Chroma(
            collection_name="cli_sage_collection",
            embedding_function=self.embeddings,
            persist_directory=Constants.CHROMA_DB_PATH,  # Where to save data locally
        )
        return vector_store