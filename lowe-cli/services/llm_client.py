from typing import Any, Union, Optional
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.constants import START
from langgraph.graph import StateGraph
from typing_extensions import List, TypedDict
from services.vector_db.chroma_service import ChromaService
from utils.constants import Constants
from langchain_core.documents import Document

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


class LlmClient:
    _instance: Optional['LlmClient'] = None
    _model: Any = None
    
    def __new__(cls) -> 'LlmClient':
        if cls._instance is None:
            cls._instance = super(LlmClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self) -> None:
        if not self._initialized:
            self.model_name: str = Constants.MODEL_NAME
            self.model_provider: str = Constants.MODEL_PROVIDER
            self._model = init_chat_model(self.model_name, model_provider=self.model_provider)
            self._initialized: bool = True
    
    @classmethod
    def get_instance(cls) -> 'LlmClient':
        """Get the singleton instance of LlmClient."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def invoke(self, user_prompt: Union[str, List[BaseMessage]], system_prompt: Optional[str] = None) -> BaseMessage:
        if system_prompt is None:
            message = user_prompt
        else:
            message = [
                SystemMessage(system_prompt),
                HumanMessage(user_prompt),
            ]
        model_response: BaseMessage = self._model.invoke(message)
        return model_response

    def retrieve_and_invoke(self, user_message: str, system_prompt: Optional[str] = None) -> str:
        graph_builder: StateGraph = StateGraph(State).add_sequence([self.retrieve, self.generate])
        graph_builder.add_edge(START, "retrieve")
        graph = graph_builder.compile()
        response: dict[str, Any] = graph.invoke({"question": user_message})
        return response["answer"]

    # Define application steps
    def retrieve(self, state: State) -> dict[str, List[Document]]:
        chroma_service: ChromaService = ChromaService()
        retrieved_docs: List[Document] = chroma_service.search(state["question"])
        return {"context": retrieved_docs}

    def generate(self, state: State) -> dict[str, str]:
        prompt_template: ChatPromptTemplate = ChatPromptTemplate([
            ("system", Constants.RAG_PROMPT),
            ("user", Constants.RAG_USER_PROMPT)
        ])
        docs_content: str = "\n\n".join(doc.page_content for doc in state["context"])
        messages = prompt_template.invoke({"question": state["question"], "context": docs_content})
        response: BaseMessage = self.invoke(messages)
        return {"answer": response.content}
