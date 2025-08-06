"""Input validation and cleaning utilities."""
from typing import List, Callable, Optional
from services.ui.ui_service import UIService


class InputValidator:
    """Handles input validation and cleaning operations."""
    
    def __init__(self, max_input_size: int = 5000, max_lines: int = 1000) -> None:
        """
        Initialize input validator.
        
        Args:
            max_input_size: Maximum input size in characters
            max_lines: Maximum number of lines to accept
        """
        self.max_input_size: int = max_input_size
        self.max_lines: int = max_lines
    
    def clean_input(self, lines: List[str]) -> str:
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
    
    def validate_choices(self, response: str, choices: List[str], 
                        case_sensitive: bool = False) -> Optional[str]:
        """
        Validate user response against available choices.
        
        Args:
            response: User's response
            choices: List of valid choices
            case_sensitive: Whether choices are case sensitive
            
        Returns:
            Valid choice or None if invalid
        """
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
        return None
    
    def validate_with_function(self, input_text: str, 
                             validator: Callable[[str], bool]) -> bool:
        """
        Validate input using a custom validation function.
        
        Args:
            input_text: Text to validate
            validator: Validation function
            
        Returns:
            True if valid, False otherwise
        """
        try:
            return validator(input_text)
        except Exception:
            return False
    
    def is_within_limits(self, lines: List[str]) -> bool:
        """
        Check if input is within size and line limits.
        
        Args:
            lines: List of input lines
            
        Returns:
            True if within limits, False otherwise
        """
        if len(lines) > self.max_lines:
            return False
        
        total_chars = sum(len(line) for line in lines) + len(lines)
        return total_chars <= self.max_input_size
