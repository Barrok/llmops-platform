from app.services.agent.service import AgentService
from app.services.llm.ollama import OllamaClient


def get_llm_client() -> OllamaClient:
    return OllamaClient()


def get_agent_service() -> AgentService:
    return AgentService(llm_client=get_llm_client())
