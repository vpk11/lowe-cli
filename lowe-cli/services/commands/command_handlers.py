"""Simplified command handlers using modular command factory."""
from services.commands.command_factory import CommandFactory


class CommandHandlers:
    """Simplified handlers for different CLI commands using modular architecture."""
    
    _factory: CommandFactory = CommandFactory()
    
    @staticmethod
    def help(user_message: str) -> None:
        """Handle help command."""
        CommandHandlers._factory.execute_command('help', user_message)
    
    @staticmethod
    def perform(user_message: str) -> None:
        """Handle perform command."""
        CommandHandlers._factory.execute_command('perform', user_message)

    @staticmethod
    def lookup(user_message: str) -> None:
        """Handle lookup command."""
        CommandHandlers._factory.execute_command('lookup', user_message)

    @staticmethod
    def index() -> None:
        """Handle index command."""
        CommandHandlers._factory.execute_command('index')
