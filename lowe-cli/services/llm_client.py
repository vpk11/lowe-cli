from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
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
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LlmClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.model_name = Constants.MODEL_NAME
            self.model_provider = Constants.MODEL_PROVIDER
            self._model = init_chat_model(self.model_name, model_provider=self.model_provider)
            self._initialized = True
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance of LlmClient."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def invoke(self, user_prompt, system_prompt=None):
        if system_prompt is None:
            message = user_prompt
        else:
            message = [
                SystemMessage(system_prompt),
                HumanMessage(user_prompt),
            ]
        model_response = self._model.invoke(message)
        return model_response

    def retrieve_and_invoke(self, user_message, system_prompt=None):
        graph_builder = StateGraph(State).add_sequence([self.retrieve, self.generate])
        graph_builder.add_edge(START, "retrieve")
        graph = graph_builder.compile()
        response = graph.invoke({"question": user_message})
        return response["answer"]

    # Define application steps
    def retrieve(self, state: State):
        chroma_service = ChromaService()
        retrieved_docs = chroma_service.search(state["question"])
        return {"context": retrieved_docs}

    def generate(self, state: State):
        prompt_template = ChatPromptTemplate([
            ("system", Constants.RAG_PROMPT),
            ("user", Constants.RAG_USER_PROMPT)
        ])
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        messages = prompt_template.invoke({"question": state["question"], "context": docs_content})
        response = self.invoke(messages)
        return {"answer": response.content}
