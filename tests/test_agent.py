from app.services.agent.service import AgentService
from app.services.llm.base import LLMClient


class FakeLLMClient(LLMClient):
    def generate(self, prompt: str) -> str:
        return f"Fake response for: {prompt}"


def test_agent_chat():
    agent = AgentService(llm_client=FakeLLMClient())

    response = agent.chat("Hello")

    assert response == "Fake response for: Hello"
