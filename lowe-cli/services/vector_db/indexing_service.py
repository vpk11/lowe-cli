from typing import Union, List
from langchain_core.documents import Document
from services.text_splitter.splitter_service import SplitterService
from services.vector_db.chroma_service import ChromaService
from services.web_base_loader.loader_service import LoaderService

# Type alias for JSON data (matching the text_splitter service)
JsonData = Union[dict, list, str, int, float, bool, None]


class IndexingService:
    """Service to handle indexing operations."""

    @staticmethod
    def index_documents(urls: str) -> None:
        """
        Index documents from a web source.
        
        Args:
            urls: The URL to load documents from
        """
        docs: JsonData = LoaderService.load(urls)
        all_splits: List[Document] = SplitterService.split_json(docs)
        ChromaService().add(all_splits)