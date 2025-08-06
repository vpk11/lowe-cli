from typing import Dict, Any
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import BaseMessage
from services.llm_client import LlmClient
from utils.constants import Constants


class ChatManagement:
    def __init__(self) -> None:
        self.chats_by_session_id: Dict[str, InMemoryChatMessageHistory] = {}
        self.llm_client: LlmClient = LlmClient.get_instance()

    def call_model(self, state: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        if "configurable" not in config or "session_id" not in config["configurable"]:
            raise ValueError(
                "Make sure that the config includes the following information: {'configurable': {'session_id': 'some_value'}}"
            )
        # Fetch the history of messages and append to it any new messages.
        chat_history: InMemoryChatMessageHistory = self.get_chat_history(config["configurable"]["session_id"])
        messages = [{"role": "system", "content": Constants.ASK_SYSTEM_PROMPT}] + list(chat_history.messages) + state["messages"]
        ai_message: BaseMessage = self.llm_client.invoke(messages)
        # Finally, update the chat message history to include
        # the new input message from the user together with the
        # response from the model.
        chat_history.add_messages(state["messages"] + [ai_message])
        return {"messages": ai_message}

    def get_chat_history(self, session_id: str) -> InMemoryChatMessageHistory:
        chat_history: InMemoryChatMessageHistory | None = self.chats_by_session_id.get(session_id)
        if chat_history is None:
            chat_history = InMemoryChatMessageHistory()
            self.chats_by_session_id[session_id] = chat_history
        return chat_history
