import uuid
import os
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.constants import START
from langgraph.graph import StateGraph, MessagesState
from rich import print as rich_print
from rich.console import Console
from rich.markdown import Markdown
from yaspin import yaspin
import subprocess
from services.chat_management import ChatManagement
from services.llm_client import LlmClient
from services.vector_db.indexing_service import IndexingService
from utils.constants import Constants


class LoweCli:
    @staticmethod
    def ask():
        session_id = uuid.uuid4()
        config = {"configurable": {"session_id": session_id}}
        builder = StateGraph(state_schema=MessagesState)
        builder.add_edge(START, "model")
        builder.add_node("model", ChatManagement().call_model)
        graph = builder.compile()

        while True:
            rich_print("[bold green]lowe-cli:bulb:[/bold green][yellow]>[/yellow] ", end="")
            lines = []
            while True:
                try:
                    line = input()
                except EOFError:
                    rich_print("\nbye byes :boom:")
                    return
                if not line:
                    break
                lines.append(line)

            cmd = "\n".join(lines).strip()

            if not cmd:
                # rich_print("[bold red]Empty input. Please enter a question or command.[/bold red]")
                continue

            if cmd.lower() in ("exit", "quit"):
                rich_print("bye byes :boom:")
                break

            input_message = HumanMessage(content=cmd)
            with yaspin(text="Thinking", color="yellow") as spinner:
                for event in graph.stream({"messages": [input_message]}, config, stream_mode="values"):
                    last_message = event["messages"][-1]
                    if isinstance(last_message, AIMessage):
                        console = Console()
                        md = Markdown(last_message.content)
                        spinner.ok("💡 ")
                        console.print(md)

    @staticmethod
    def help(user_message):
        user_message = user_message.strip()
        if not user_message:
            rich_print("[bold red]Please enter a valid question for help.[/bold red]")
            return

        console = Console()
        with yaspin(text="Thinking", color="yellow") as spinner:
            response = LlmClient().invoke(user_message, Constants.HELP_SYSTEM_PROMPT)
            md = Markdown(response.content)
            spinner.ok("💡 ")
            console.print(md)
    
    @staticmethod
    def perform(user_message):
        user_message = user_message.strip()
        if not user_message:
            rich_print("[bold red]Please enter a valid instruction to perform.[/bold red]")
            return
        prompt_template = ChatPromptTemplate([
            ("system", Constants.PERFORM_SYSTEM_PROMPT),
            ("user", Constants.RAG_USER_PROMPT)
        ])

        messages = prompt_template.invoke({"question": user_message, "context": LoweCli.get_history()})
        with yaspin(text="Thinking", color="yellow") as spinner:
            response = LlmClient().invoke(messages)
            spinner.ok("💡 ")
            rich_print(f"[green]{response.content}[/green]")

    @staticmethod
    def lookup(user_message):
        console = Console()
        with yaspin(text="Thinking", color="yellow") as spinner:
            response = LlmClient().retrieve_and_invoke(user_message, Constants.LOOKUP_SYSTEM_PROMPT)
            md = Markdown(response)
            spinner.ok("💡 ")
            console.print(md)

    @staticmethod
    def index():
        if not os.path.exists("./chroma_langchain_db"):
            with yaspin(text="Indexing", color="yellow") as spinner:
                IndexingService.index_documents(Constants.KNOWLEDGE_BASE)
                spinner.ok("💡 ")

    @staticmethod
    def get_history():
        """Run `history --reverse --max 100` and return output as a list of strings."""
        result = subprocess.run(
            "history | tail -r | head -n 100",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
            executable="/bin/bash"
        )
        return "\n".join(line.strip() for line in result.stdout.splitlines() if line.strip())