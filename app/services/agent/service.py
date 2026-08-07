from app.services.llm.base import LLMClient


class AgentService:
    """Core agent orchestration service."""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def chat(self, message: str) -> str:
        return self.llm_client.generate(message)
