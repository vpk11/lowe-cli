from langchain_huggingface import HuggingFaceEmbeddings

class EmbeddingModelService:
    """Service to get HuggingFace embeddings model."""

    @staticmethod
    def get_huggingface_embeddings(model_name="sentence-transformers/all-mpnet-base-v2"):
        """Get HuggingFace embeddings model."""

        embeddings = HuggingFaceEmbeddings(model_name=model_name)
        return embeddings