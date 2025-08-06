from langchain_chroma import Chroma
from services.huggingface.embedding_model_service import EmbeddingModelService
from utils.constants import Constants


class ChromaService:
    """Service to handle Chroma vector database operations."""
    def __init__(self):
        """Initialize the ChromaService with the specified embeddings model."""
        self.embeddings = EmbeddingModelService.get_huggingface_embeddings()

    def add(self, documents):
        """Add documents to the Chroma vector store."""

        vector_store = self.__vector_store()
        vector_store.add_documents(documents=documents)

    def search(self, query, k=5):
        """Search for similar documents in the Chroma vector store."""

        vector_store = self.__vector_store()
        retrieved_docs = vector_store.similarity_search(query)
        return retrieved_docs

    def __vector_store(self):
        """Get Chroma embeddings model."""

        vector_store = Chroma(
            collection_name="cli_sage_collection",
            embedding_function=self.embeddings,
            persist_directory=Constants.CHROMA_DB_PATH,  # Where to save data locally
        )
        return vector_store