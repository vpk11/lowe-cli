"""Lookup command handler."""
from services.commands.base_command_handler import BaseCommandHandler
from services.llm_client import LlmClient
from services.ui.ui_service import UIService
from utils.constants import Constants


class LookupCommandHandler(BaseCommandHandler):
    """Handler for lookup command operations."""
    
    def execute(self, user_message: str) -> None:
        """
        Execute lookup command to search and retrieve information from the knowledge base.
        
        Args:
            user_message: The search query from the user
        """
        def execute_lookup():
            return LlmClient().retrieve_and_invoke(user_message, Constants.LOOKUP_SYSTEM_PROMPT)

        content = UIService.execute_with_spinner(execute_lookup)
        UIService.render_markdown(content)
