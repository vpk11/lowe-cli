"""Perform command handler."""
from langchain_core.prompts import ChatPromptTemplate
from services.commands.base_command_handler import BaseCommandHandler
from services.llm_client import LlmClient
from services.history.history_service import HistoryService
from services.ui.ui_service import UIService
from utils.constants import Constants


class PerformCommandHandler(BaseCommandHandler):
    """Handler for perform command operations."""
    
    def __init__(self):
        """Initialize the perform command handler with prompt template and shared LlmClient instance."""
        self.prompt_template = ChatPromptTemplate([
            ("system", Constants.PERFORM_SYSTEM_PROMPT),
            ("user", Constants.RAG_USER_PROMPT)
        ])
        self.llm_client = LlmClient.get_instance()
    
    def execute(self, user_message: str) -> None:
        """
        Execute perform command to generate shell commands based on user instructions.
        
        Args:
            user_message: The instruction from the user
        """
        try:
            user_message = self.validate_input(
                user_message, 
                "Please enter a valid instruction to perform."
            )
        except ValueError:
            return

        def execute_perform():
            messages = self.prompt_template.invoke({
                "question": user_message, 
                "context": HistoryService.get_recent_history()
            })
            response = self.llm_client.invoke(messages)
            return response.content

        content = UIService.execute_with_spinner(execute_perform)
        UIService.print_success(content)
