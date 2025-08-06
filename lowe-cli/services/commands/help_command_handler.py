"""Help command handler."""
from services.commands.base_command_handler import BaseCommandHandler
from services.llm_client import LlmClient
from services.ui.ui_service import UIService
from utils.constants import Constants


class HelpCommandHandler(BaseCommandHandler):
    """Handler for help command operations."""
    
    def execute(self, user_message: str) -> None:
        """
        Execute help command to provide assistance and explanations.
        
        Args:
            user_message: The help query from the user
        """
        try:
            user_message = self.validate_input(
                user_message, 
                "Please enter a valid question for help."
            )
        except ValueError:
            return

        def execute_help():
            response = LlmClient().invoke(user_message, Constants.HELP_SYSTEM_PROMPT)
            return response.content

        content = UIService.execute_with_spinner(execute_help)
        UIService.render_markdown(content)
