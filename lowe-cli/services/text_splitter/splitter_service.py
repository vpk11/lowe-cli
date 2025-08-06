from typing import List, Union
from langchain_text_splitters import RecursiveJsonSplitter
from langchain_core.documents import Document

# Type alias for JSON data
JsonData = Union[dict, list, str, int, float, bool, None]


class SplitterService:
    """Service to handle json splitting operations."""

    @staticmethod
    def split_json(json_data: JsonData) -> List[Document]:
        """
        Split JSON data into smaller chunks using RecursiveJsonSplitter.
        
        Args:
            json_data: The JSON data to split (can be dict, list, str, int, float, bool, or None)
            
        Returns:
            List of Document objects containing the split data
        """
        splitter: RecursiveJsonSplitter = RecursiveJsonSplitter(max_chunk_size=300)
        docs: List[Document] = splitter.create_documents(texts=[json_data])
        return docs