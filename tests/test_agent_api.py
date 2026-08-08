from fastapi.testclient import TestClient

from app.dependencies.providers import get_agent_service
from app.main import app
from app.services.agent.conversation import ConversationManager
from app.services.agent.prompts import PromptManager
from app.services.agent.service import AgentService
from app.services.llm.base import LLMClient


class FakeAgentService:
    def chat(self, conversation_id: str, message: str) -> str:
        assert conversation_id == "conversation-1"
        assert message == "Hello"

        return "fake response"


def override_get_agent_service():
    return FakeAgentService()


app.dependency_overrides[get_agent_service] = override_get_agent_service


client = TestClient(app)


def teardown_module():
    app.dependency_overrides.clear()


def test_agent_chat_endpoint():
    response = client.post(
        "/agent/chat",
        json={
            "conversation_id": "conversation-1",
            "message": "Hello",
        },
    )

    print(response.json())

    assert response.status_code == 200
    assert "response" in response.json()


def test_agent_chat_endpoint_preserves_conversation_id():
    calls = []

    class FakeAgentService:
        def chat(self, conversation_id: str, message: str) -> str:
            calls.append((conversation_id, message))
            return "fake response"

    app.dependency_overrides[get_agent_service] = lambda: FakeAgentService()

    try:
        first_response = client.post(
            "/agent/chat",
            json={
                "conversation_id": "conversation-1",
                "message": "Hello",
            },
        )

        second_response = client.post(
            "/agent/chat",
            json={
                "conversation_id": "conversation-1",
                "message": "How are you?",
            },
        )

        assert first_response.status_code == 200
        assert second_response.status_code == 200

        assert calls == [
            ("conversation-1", "Hello"),
            ("conversation-1", "How are you?"),
        ]
    finally:
        app.dependency_overrides.clear()


def test_agent_chat_endpoint_integrates_with_agent_service():
    class FakeLLMClient(LLMClient):
        def generate(self, messages: list[dict[str, str]]) -> str:
            return f"Response {len(messages)}"

    fake_agent = AgentService(
        llm_client=FakeLLMClient(),
        prompt_manager=PromptManager(),
        conversation_manager=ConversationManager(),
    )

    app.dependency_overrides[get_agent_service] = lambda: fake_agent

    try:
        first_response = client.post(
            "/agent/chat",
            json={
                "conversation_id": "conversation-1",
                "message": "Hello",
            },
        )

        second_response = client.post(
            "/agent/chat",
            json={
                "conversation_id": "conversation-1",
                "message": "How are you?",
            },
        )

        assert first_response.status_code == 200
        assert first_response.json() == {"response": "Response 2"}

        assert second_response.status_code == 200
        assert second_response.json() == {"response": "Response 4"}
    finally:
        app.dependency_overrides.clear()
