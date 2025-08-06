"""Terminal utility functions for CLI operations."""
import sys
import os
from typing import Tuple


class TerminalUtils:
    """Utility class for terminal-related operations."""
    
    @staticmethod
    def is_tty() -> bool:
        """Check if input is from a terminal (TTY)."""
        try:
            return os.isatty(sys.stdin.fileno())
        except (OSError, AttributeError):
            return False
    
    @staticmethod
    def get_terminal_size() -> Tuple[int, int]:
        """
        Get terminal size for formatting purposes.
        
        Returns:
            Tuple of (columns, lines)
        """
        try:
            size = os.get_terminal_size()
            return (size.columns, size.lines)
        except OSError:
            # Fallback for non-terminal environments
            return (80, 24)
    
    @staticmethod
    def supports_colors() -> bool:
        """Check if terminal supports colors."""
        return (
            hasattr(sys.stdout, 'isatty') and 
            sys.stdout.isatty() and 
            os.environ.get('TERM') != 'dumb'
        )
