from fastapi.testclient import TestClient

from app.dependencies.providers import get_agent_service
from app.main import app


class FakeAgentService:
    def chat(self, message: str) -> str:
        return f"Fake answer for: {message}"


def override_get_agent_service():
    return FakeAgentService()


app.dependency_overrides[get_agent_service] = override_get_agent_service


client = TestClient(app)


def test_agent_chat_endpoint():
    response = client.post(
        "/agent/chat",
        json={"message": "Hello agent"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["response"] == "Fake answer for: Hello agent"


def teardown_module():
    app.dependency_overrides.clear()
