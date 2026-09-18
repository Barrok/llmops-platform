from app.config.settings import settings
from app.services.agent.conversation import ConversationManager
from app.services.agent.prompts import PromptManager
from app.services.agent.service import AgentService
from app.services.embeddings.ollama import OllamaEmbeddingClient
from app.services.embeddings.service import EmbeddingService
from app.services.llm.ollama import OllamaClient
from app.services.rag.context import ContextBuilder
from app.services.retrieval.service import RetrievalService
from app.services.vector_store.qdrant import QdrantVectorStore


def get_llm_client() -> OllamaClient:
    return OllamaClient()


def get_prompt_manager() -> PromptManager:
    return PromptManager()


def get_conversation_manager() -> ConversationManager:
    return ConversationManager()


def get_embedding_service() -> EmbeddingService:
    return EmbeddingService(
        client=OllamaEmbeddingClient(base_url=settings.OLLAMA_BASE_URL),
    )


def get_vector_store() -> QdrantVectorStore:
    return QdrantVectorStore(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT,
    )


def get_retrieval_service() -> RetrievalService:
    return RetrievalService(
        embedding_service=get_embedding_service(),
        retriever=get_vector_store(),
    )


def get_agent_service() -> AgentService:
    return AgentService(
        llm_client=get_llm_client(),
        prompt_manager=get_prompt_manager(),
        conversation_manager=get_conversation_manager(),
        retrieval_service=get_retrieval_service(),
        context_builder=ContextBuilder(),
    )
