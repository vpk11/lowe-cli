"""Base input handler with core functionality."""
from typing import Optional
from services.ui.ui_service import UIService
from .terminal_utils import TerminalUtils


class BaseInputHandler:
    """Base class for handling user input with common functionality."""
    
    def __init__(self, prompt: str = ""):
        """
        Initialize base input handler.
        
        Args:
            prompt: Default prompt to display
        """
        self.prompt = prompt
    
    def _handle_input_exceptions(self, operation_name: str = "input") -> None:
        """
        Common exception handling for input operations.
        
        Args:
            operation_name: Name of the operation for error messages
        """
        # This method would be used in derived classes
        pass
    
    def _get_safe_input(self, prompt_text: str = "") -> Optional[str]:
        """
        Safely get a single line of input with proper exception handling.
        
        Args:
            prompt_text: Prompt to display
            
        Returns:
            User input or None if error/cancellation
        """
        try:
            return input(prompt_text)
        except EOFError:
            return None
        except KeyboardInterrupt:
            return None
        except (OSError, IOError, UnicodeError, ValueError) as e:
            UIService.print_error(f"Error reading input: {e}")
            return None
    
    def confirm_action(self, message: str, default: bool = False) -> bool:
        """
        Ask user for yes/no confirmation.
        
        Args:
            message: Confirmation message to display
            default: Default value if user just presses enter
            
        Returns:
            True for yes, False for no
        """
        suffix = " [Y/n]" if default else " [y/N]"
        prompt_text = f"{message}{suffix}: "
        
        response = self._get_safe_input(prompt_text)
        if response is None:
            return False
        
        response = response.strip().lower()
        if not response:
            return default
        
        return response in ('y', 'yes', 'true', '1')
    
    def ask_retry(self, message: str) -> bool:
        """Ask user if they want to retry an operation."""
        return self.confirm_action(message, default=True)
    
    def is_terminal_available(self) -> bool:
        """Check if running in a terminal environment."""
        return TerminalUtils.is_tty()
