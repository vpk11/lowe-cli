"""UI Service for handling common UI patterns and interactions."""
from rich import print as rich_print
from rich.console import Console
from rich.markdown import Markdown
from yaspin import yaspin
from typing import Any, Callable


class UIService:
    """Service for handling common UI operations."""
    
    @staticmethod
    def print_error(message: str) -> None:
        """Print an error message in red."""
        rich_print(f"[bold red]{message}[/bold red]")
    
    @staticmethod
    def print_success(message: str) -> None:
        """Print a success message in green."""
        rich_print(f"[green]{message}[/green]")
    
    @staticmethod
    def print_info(message: str) -> None:
        """Print an info message in blue."""
        rich_print(f"[blue]{message}[/blue]")
    
    @staticmethod
    def print_prompt() -> None:
        """Print the CLI prompt."""
        rich_print("[bold green]lowe-cli:bulb:[/bold green][yellow]>[/yellow] ", end="")
    
    @staticmethod
    def print_goodbye() -> None:
        """Print goodbye message."""
        rich_print("bye bye 💥")
    
    @staticmethod
    def render_markdown(content: str) -> None:
        """Render markdown content to the console."""
        console = Console()
        md = Markdown(content)
        console.print(md)
    
    @staticmethod
    def with_spinner(text: str, color: str = "yellow") -> yaspin:
        """Create a spinner with standard success icon."""
        return yaspin(text=text, color=color)
    
    @staticmethod
    def execute_with_spinner(
        func: Callable[[], Any], 
        text: str = "Thinking", 
        color: str = "yellow"
    ) -> Any:
        """Execute a function with a spinner and return the result."""
        with UIService.with_spinner(text, color) as spinner:
            result = func()
            spinner.ok("💡 ")
            return result
