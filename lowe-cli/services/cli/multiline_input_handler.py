"""Multiline input handler for CLI operations."""
from typing import Optional, List
from services.ui.ui_service import UIService
from .base_input_handler import BaseInputHandler
from .input_validator import InputValidator


class MultilineInputHandler(BaseInputHandler):
    """Handles multi-line input operations."""
    
    def __init__(self, prompt: str = "", max_input_size: int = 5000, max_lines: int = 1000) -> None:
        """
        Initialize multiline input handler.
        
        Args:
            prompt: Default prompt to display
            max_input_size: Maximum input size in characters
            max_lines: Maximum number of lines to accept
        """
        super().__init__(prompt)
        self.validator: InputValidator = InputValidator(max_input_size, max_lines)
        self._shown_help: bool = False
    
    def get_input(self, max_lines: Optional[int] = None, 
                  custom_prompt: Optional[str] = None) -> Optional[str]:
        """
        Get multi-line input from user until empty line is entered.
        
        Args:
            max_lines: Maximum number of lines to accept (overrides default)
            custom_prompt: Custom prompt for this specific input
            
        Returns:
            Cleaned user input or None if user wants to exit
        """
        effective_max_lines = max_lines or self.validator.max_lines
        lines: List[str] = []
        line_count = 0
        
        self._show_help_if_needed(custom_prompt)
        
        try:
            while line_count < effective_max_lines:
                line = self._get_line_input(line_count)
                if line is None:
                    # Handle EOF or cancellation
                    if not lines:
                        UIService.print_goodbye()
                        return None
                    break
                
                # Empty line ends input
                if not line:
                    break
                    
                lines.append(line)
                line_count += 1
            
            if line_count >= effective_max_lines:
                UIService.print_error(f"Input too long (max {effective_max_lines} lines)")
                if self.ask_retry("Input was too long. Try again?"):
                    return self.get_input(max_lines, custom_prompt)
                return None
                
        except (OSError, IOError, UnicodeError, ValueError) as e:
            UIService.print_error(f"Error reading input: {e}")
            return None
        
        return self.validator.clean_input(lines)
    
    def _show_help_if_needed(self, custom_prompt: Optional[str]) -> None:
        """Show help hint for first-time users."""
        if custom_prompt:
            print(custom_prompt)
        elif not self._shown_help:
            UIService.print_info("Enter your input (empty line to finish, Ctrl+C to cancel, Ctrl+D to exit):")
            self._shown_help = True
    
    def _get_line_input(self, line_count: int) -> Optional[str]:
        """Get a single line of input with appropriate prompt."""
        try:
            if line_count > 5:
                return input(f"{line_count + 1:3d}> ")
            else:
                return input()
        except EOFError:
            return None
        except KeyboardInterrupt:
            raise  # Let it propagate to CLI interface
        except (OSError, IOError, UnicodeError, ValueError):
            return None
