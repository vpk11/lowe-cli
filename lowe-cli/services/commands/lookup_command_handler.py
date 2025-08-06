"""Lookup command handler."""
from services.commands.base_command_handler import BaseCommandHandler
from services.llm_client import LlmClient
from services.ui.ui_service import UIService
from utils.constants import Constants


class LookupCommandHandler(BaseCommandHandler):
    """Handler for lookup command operations."""
    
    def __init__(self) -> None:
        """Initialize the lookup command handler with a shared LlmClient instance."""
        self.llm_client: LlmClient = LlmClient.get_instance()
    
    def execute(self, user_message: str) -> None:
        """
        Execute lookup command to search and retrieve information from the knowledge base.
        
        Args:
            user_message: The search query from the user
        """
        def execute_lookup() -> str:
            return self.llm_client.retrieve_and_invoke(user_message, Constants.LOOKUP_SYSTEM_PROMPT)

        content: str = UIService.execute_with_spinner(execute_lookup)
        UIService.render_markdown(content)
