from app.services.agent.conversation import ConversationManager
from app.services.agent.prompts import PromptManager
from app.services.agent.service import AgentService
from app.services.llm.ollama import OllamaClient


def get_llm_client() -> OllamaClient:
    return OllamaClient()


def get_prompt_manager() -> PromptManager:
    return PromptManager()


def get_conversation_manager() -> ConversationManager:
    return ConversationManager()


_agent_service = AgentService(
    llm_client=get_llm_client(),
    prompt_manager=get_prompt_manager(),
    conversation_manager=get_conversation_manager(),
)


def get_agent_service() -> AgentService:
    return _agent_service
