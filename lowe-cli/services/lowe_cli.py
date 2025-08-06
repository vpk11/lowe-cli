"""Simplified and modular LoweCli class."""
from services.cli.cli_interface import CLIInterface
from services.commands.command_handlers import CommandHandlers


class LoweCli:
    """Main CLI application class with simplified, modular design."""
    
    @staticmethod
    def ask() -> None:
        """Start the interactive CLI session."""
        cli: CLIInterface = CLIInterface()
        cli.run()

    @staticmethod
    def help(user_message: str) -> None:
        """Handle help command."""
        CommandHandlers.help(user_message)
    
    @staticmethod
    def perform(user_message: str) -> None:
        """Handle perform command."""
        CommandHandlers.perform(user_message)

    @staticmethod
    def lookup(user_message: str) -> None:
        """Handle lookup command."""
        CommandHandlers.lookup(user_message)

    @staticmethod
    def index() -> None:
        """Handle index command."""
        CommandHandlers.index()