"""Input handler for CLI operations following Python best practices."""
from typing import Optional, List, TYPE_CHECKING
from .multiline_input_handler import MultilineInputHandler
from .terminal_utils import TerminalUtils

if TYPE_CHECKING:
    import os


class InputHandler:
    """
    Handles user input with proper signal handling and validation.
    
    This class has been simplified to only include the functionality 
    actually used by the application (multiline input).
    """
    
    def __init__(self, prompt: str = "", max_input_size: int = 5000, max_lines: int = 1000) -> None:
        """
        Initialize input handler.
        
        Args:
            prompt: Custom prompt to display (optional)
            max_input_size: Maximum input size in characters
            max_lines: Maximum number of lines to accept
        """
        self.prompt: str = prompt
        self.max_input_size: int = max_input_size
        self.max_lines: int = max_lines
        
        # Initialize only the multiline handler (the only one actually used)
        self._multiline_handler: MultilineInputHandler = MultilineInputHandler(prompt, max_input_size, max_lines)
    
    def get_multiline_input(self, max_lines: Optional[int] = None, 
                           custom_prompt: Optional[str] = None) -> Optional[str]:
        """
        Get multi-line input from user until empty line is entered.
        
        Args:
            max_lines: Maximum number of lines to accept (overrides default)
            custom_prompt: Custom prompt for this specific input
            
        Returns:
            Cleaned user input or None if user wants to exit
        """
        return self._multiline_handler.get_input(max_lines, custom_prompt)
    
    # Legacy methods for backward compatibility (no longer used but kept to avoid breaking changes)
    def _ask_retry(self, message: str) -> bool:
        """Ask user if they want to retry an operation."""
        return self._multiline_handler.ask_retry(message)
    
    def _clean_input(self, lines: List[str]) -> str:
        """Clean and validate input lines."""
        return self._multiline_handler.validator.clean_input(lines)
    
    def is_tty(self) -> bool:
        """Check if input is from a terminal (TTY)."""
        return TerminalUtils.is_tty()
    
    def get_terminal_size(self) -> "os.terminal_size[int]":
        """Get terminal size for formatting purposes."""
        cols, lines = TerminalUtils.get_terminal_size()
        # Return in the original format for backward compatibility
        import os
        return os.terminal_size((cols, lines))
