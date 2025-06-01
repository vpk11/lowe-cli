from langchain_text_splitters import RecursiveJsonSplitter


class SplitterService:
    """Service to handle json splitting operations."""

    @staticmethod
    def split_json(json_data):
        splitter = RecursiveJsonSplitter(max_chunk_size=300)
        docs = splitter.create_documents(texts=[json_data])
        return docs