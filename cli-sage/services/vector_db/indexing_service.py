from services.text_splitter.splitter_service import SplitterService
from services.vector_db.chroma_service import ChromaService
from services.web_base_loader.loader_service import LoaderService


class IndexingService:
    """Service to handle indexing operations."""

    @staticmethod
    def index_documents(urls):
        """Index documents from a web source."""
        docs = LoaderService.load(urls)
        all_splits = SplitterService.split_json(docs)
        ChromaService().add(all_splits)