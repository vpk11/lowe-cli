"""Base command handler class for common functionality."""
from abc import ABC, abstractmethod
from services.ui.ui_service import UIService


class BaseCommandHandler(ABC):
    """Abstract base class for command handlers."""
    
    def validate_input(self, user_message: str, error_msg: str) -> str:
        """
        Validate and clean user input.
        
        Args:
            user_message: The user input to validate
            error_msg: Error message to display if input is invalid
            
        Returns:
            Cleaned user message
            
        Raises:
            ValueError: If input is invalid
        """
        user_message = user_message.strip()
        if not user_message:
            UIService.print_error(error_msg)
            raise ValueError("Invalid input")
        return user_message
    
    @abstractmethod
    def execute(self, user_message: str) -> None:
        """Execute the command with the given user message."""
        pass
