"""Input handler for CLI operations following Python best practices."""
import sys
import signal
import os
from typing import Optional, List, Callable
from services.ui.ui_service import UIService


class InputHandler:
    """Handles user input with proper signal handling and validation."""
    
    def __init__(self, prompt: str = "", max_input_size: int = 5000, max_lines: int = 1000):
        """
        Initialize input handler.
        
        Args:
            prompt: Custom prompt to display (optional)
            max_input_size: Maximum input size in characters
            max_lines: Maximum number of lines to accept
        """
        self.prompt = prompt
        self.max_input_size = max_input_size
        self.max_lines = max_lines
        self._original_sigint_handler = None
        self._setup_signal_handlers()
    
    def _setup_signal_handlers(self) -> None:
        """Setup signal handlers for graceful interruption handling."""
        # For Ctrl+C, we'll let Python's default KeyboardInterrupt handling work
        # and just catch it in our input methods. This is simpler and more reliable.
        pass
    
    def restore_signal_handlers(self) -> None:
        """Restore original signal handlers."""
        if self._original_sigint_handler:
            signal.signal(signal.SIGINT, self._original_sigint_handler)
    
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
        effective_max_lines = max_lines or self.max_lines
        lines: List[str] = []
        line_count = 0
        
        # Show help hint for first-time users
        if custom_prompt:
            print(custom_prompt)
        elif not hasattr(self, '_shown_multiline_help'):
            print("Enter your input (empty line to finish, Ctrl+C to cancel, Ctrl+D to exit):")
            self._shown_multiline_help = True
        
        try:
            while line_count < effective_max_lines:
                try:
                    # Show line number for long inputs
                    if line_count > 5:
                        line = input(f"{line_count + 1:3d}> ")
                    else:
                        line = input()
                except EOFError:
                    # Handle Ctrl+D gracefully
                    if not lines:
                        # EOF on first line means exit
                        UIService.print_goodbye()
                        return None
                    # EOF with existing input, treat as submission
                    break
                except KeyboardInterrupt:
                    # Ctrl+C pressed - let it propagate to CLI interface
                    raise
                
                # Empty line ends input
                if not line:
                    break
                    
                lines.append(line)
                line_count += 1
            
            if line_count >= effective_max_lines:
                UIService.print_error(f"Input too long (max {effective_max_lines} lines)")
                if self._ask_retry("Input was too long. Try again?"):
                    return self.get_multiline_input(max_lines, custom_prompt)
                return None
                
        except Exception as e:
            UIService.print_error(f"Error reading input: {e}")
            return None
        
        return self._clean_input(lines)
    
    def get_single_line_input(self, custom_prompt: Optional[str] = None, 
                             strip_whitespace: bool = True,
                             validator: Optional[Callable[[str], bool]] = None) -> Optional[str]:
        """
        Get single line input from user.
        
        Args:
            custom_prompt: Custom prompt for this input
            strip_whitespace: Whether to strip leading/trailing whitespace
            validator: Optional validation function
            
        Returns:
            User input or None if user wants to exit
        """
        prompt_text = custom_prompt or self.prompt
        
        while True:
            try:
                line = input(prompt_text)
                if strip_whitespace:
                    line = line.strip()
                
                # Apply validation if provided
                if validator and line and not validator(line):
                    UIService.print_error("Invalid input. Please try again.")
                    continue
                    
                return line
            except EOFError:
                return None
            except KeyboardInterrupt:
                return None
            except Exception as e:
                UIService.print_error(f"Error reading input: {e}")
                return None
    
    def get_password_input(self, prompt_text: str = "Password: ") -> Optional[str]:
        """
        Get password input without echoing to terminal.
        
        Args:
            prompt_text: Prompt to display
            
        Returns:
            Password string or None if cancelled
        """
        try:
            import getpass
            return getpass.getpass(prompt_text)
        except (EOFError, KeyboardInterrupt):
            return None
        except Exception as e:
            UIService.print_error(f"Error reading password: {e}")
            return None
    
    def get_choice_input(self, prompt_text: str, choices: List[str], 
                        default: Optional[str] = None, case_sensitive: bool = False) -> Optional[str]:
        """
        Get input with predefined choices.
        
        Args:
            prompt_text: Prompt to display
            choices: List of valid choices
            default: Default choice if user presses enter
            case_sensitive: Whether choices are case sensitive
            
        Returns:
            Selected choice or None if cancelled
        """
        if not choices:
            raise ValueError("Choices cannot be empty")
        
        # Format choices display
        choices_display = "/".join(choices)
        if default:
            choices_display = choices_display.replace(default, default.upper())
        
        full_prompt = f"{prompt_text} [{choices_display}]: "
        
        while True:
            try:
                response = input(full_prompt).strip()
                
                if not response and default:
                    return default
                
                # Check if response matches any choice
                if case_sensitive:
                    valid_choices = choices
                    user_input = response
                else:
                    valid_choices = [choice.lower() for choice in choices]
                    user_input = response.lower()
                
                if user_input in valid_choices:
                    # Return original case choice
                    idx = valid_choices.index(user_input)
                    return choices[idx]
                else:
                    UIService.print_error(f"Please choose from: {choices_display}")
                    
            except (EOFError, KeyboardInterrupt):
                return None
            except Exception as e:
                UIService.print_error(f"Error reading input: {e}")
                return None
    
    def _ask_retry(self, message: str) -> bool:
        """Ask user if they want to retry an operation."""
        return self.confirm_action(message, default=True)
    
    def _clean_input(self, lines: List[str]) -> str:
        """
        Clean and validate input lines.
        
        Args:
            lines: List of input lines
            
        Returns:
            Cleaned and joined input string
        """
        if not lines:
            return ""
        
        # Remove excessive whitespace and join lines
        cleaned_lines = [line.rstrip() for line in lines]
        
        # Remove trailing empty lines
        while cleaned_lines and not cleaned_lines[-1]:
            cleaned_lines.pop()
        
        result = "\n".join(cleaned_lines)
        
        # Basic security: limit total input size
        if len(result) > self.max_input_size:
            UIService.print_error(f"Input too large (max {self.max_input_size} characters)")
            return ""
        
        return result
    
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
        
        try:
            response = input(prompt_text).strip().lower()
            if not response:
                return default
            return response in ('y', 'yes', 'true', '1')
        except (EOFError, KeyboardInterrupt):
            return False
    
    def is_tty(self) -> bool:
        """Check if input is from a terminal (TTY)."""
        return os.isatty(sys.stdin.fileno())
    
    def get_terminal_size(self) -> tuple:
        """Get terminal size for formatting purposes."""
        try:
            return os.get_terminal_size()
        except OSError:
            # Fallback for non-terminal environments
            return os.terminal_size((80, 24))
