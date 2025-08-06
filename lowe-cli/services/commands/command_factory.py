"""Command factory for creating and managing command handlers."""
from typing import Dict, Type
from services.commands.base_command_handler import BaseCommandHandler
from services.commands.help_command_handler import HelpCommandHandler
from services.commands.perform_command_handler import PerformCommandHandler
from services.commands.lookup_command_handler import LookupCommandHandler
from services.commands.index_command_handler import IndexCommandHandler


class CommandFactory:
    """Factory class for creating and managing command handlers."""
    
    def __init__(self):
        """Initialize the command factory with available command handlers."""
        self._handlers: Dict[str, Type[BaseCommandHandler]] = {
            'help': HelpCommandHandler,
            'perform': PerformCommandHandler,
            'lookup': LookupCommandHandler,
            'index': IndexCommandHandler
        }
    
    def get_handler(self, command_name: str) -> BaseCommandHandler:
        """
        Get a fresh command handler instance for the specified command.
        
        Args:
            command_name: Name of the command to get handler for
            
        Returns:
            Fresh command handler instance
            
        Raises:
            ValueError: If command is not supported
        """
        if command_name not in self._handlers:
            raise ValueError(f"Unsupported command: {command_name}")
        
        return self._handlers[command_name]()
    
    def execute_command(self, command_name: str, user_message: str = "") -> None:
        """
        Execute a command with the given user message.
        
        Args:
            command_name: Name of the command to execute
            user_message: User input for the command
            
        Raises:
            ValueError: If command is not supported
        """
        handler = self.get_handler(command_name)
        handler.execute(user_message)
    
    def list_available_commands(self) -> list:
        """Get a list of available command names."""
        return list(self._handlers.keys())
