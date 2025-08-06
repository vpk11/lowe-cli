"""Index command handler."""
import os
from services.commands.base_command_handler import BaseCommandHandler
from services.vector_db.indexing_service import IndexingService
from services.ui.ui_service import UIService
from utils.constants import Constants


class IndexCommandHandler(BaseCommandHandler):
    """Handler for index command operations."""
    
    def __init__(self):
        """Initialize the index command handler."""
        self.db_path = "./chroma_langchain_db"
    
    def execute(self, user_message: str = "") -> None:
        """
        Execute index command to build the document index if it doesn't exist.
        
        Args:
            user_message: Not used for index command, kept for interface consistency
        """
        if not os.path.exists(self.db_path):
            def execute_index():
                IndexingService.index_documents(Constants.KNOWLEDGE_BASE)
                return "Indexing completed"

            UIService.execute_with_spinner(execute_index, "Indexing")
        else:
            UIService.print_success("Index already exists")
