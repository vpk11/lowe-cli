"""CLI interface for handling user interactions and input processing."""
import uuid
from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.constants import START
from langgraph.graph import StateGraph, MessagesState
from services.chat_management import ChatManagement
from services.ui.ui_service import UIService
from services.cli.input_handler import InputHandler


class CLIInterface:
    """Main CLI interface for handling user interactions."""
    
    def __init__(self) -> None:
        """Initialize the CLI interface with a chat graph and input handler."""
        self.session_id: uuid.UUID = uuid.uuid4()
        self.config: Dict[str, Any] = {"configurable": {"session_id": self.session_id}}
        self.graph: StateGraph = self._build_graph()
        self.input_handler: InputHandler = InputHandler()
    
    def _build_graph(self) -> StateGraph:
        """Build and compile the chat graph."""
        builder = StateGraph(state_schema=MessagesState)
        builder.add_edge(START, "model")
        builder.add_node("model", ChatManagement().call_model)
        return builder.compile()
    
    def get_user_input(self) -> str:
        """
        Get user input following CLI best practices.
        
        Returns:
            User input string, or "exit" if user wants to quit
        """
        user_input = self.input_handler.get_multiline_input()
        
        if user_input is None:
            # User pressed Ctrl+D - InputHandler already handled goodbye
            return "exit"
        
        return user_input
    
    def should_exit(self, command: str) -> bool:
        """Check if the command indicates the user wants to exit."""
        if not command:
            return False
        return command.lower() in ("exit", "quit", "q", "bye")
    
    def validate_command(self, command: str) -> bool:
        """
        Validate command input.
        
        Args:
            command: The command to validate
            
        Returns:
            True if command is valid, False otherwise
        """
        if not command or not command.strip():
            return False
        
        # Check for potentially dangerous input
        if len(command) > 10000:  # Reasonable limit
            UIService.print_error("Command too long")
            return False
        
        return True
    
    def process_message(self, message: str) -> None:
        """Process a user message through the chat graph."""
        input_message = HumanMessage(content=message)
        
        with UIService.with_spinner("Thinking") as spinner:
            for event in self.graph.stream({"messages": [input_message]}, self.config, stream_mode="values"):
                last_message = event["messages"][-1]
                if isinstance(last_message, AIMessage):
                    spinner.ok("💡 ")
                    UIService.render_markdown(last_message.content)
    
    def run(self) -> None:
        """Run the main CLI interaction loop with improved error handling."""
        while True:
            try:
                UIService.print_prompt()
                command = self.get_user_input()
                
                # Handle exit conditions
                if self.should_exit(command):
                    # Only print goodbye if user typed exit/quit manually
                    if command != "exit":  # "exit" means Ctrl+D was pressed
                        UIService.print_goodbye()
                    break
                
                # Validate and process command
                if self.validate_command(command):
                    try:
                        self.process_message(command)
                    except Exception as e:
                        UIService.print_error(f"Error processing command: {e}")
                        
            except KeyboardInterrupt:
                # Handle Ctrl+C at any point - print newline and continue
                print()  # New line after ^C
                continue
            except Exception as e:
                UIService.print_error(f"Unexpected error: {e}")
                UIService.print_goodbye()
                break
