from app.services.agent.conversation import ConversationManager
from app.services.agent.prompts import PromptManager
from app.services.agent.service import AgentService
from app.services.llm.base import LLMClient


class FakeLLMClient(LLMClient):
    def generate(self, messages: list[dict[str, str]]) -> str:
        return f"Fake response for: {messages[-1]['content']}"


def test_agent_chat():
    agent = AgentService(
        llm_client=FakeLLMClient(),
        prompt_manager=PromptManager(),
        conversation_manager=ConversationManager(),
    )

    response = agent.chat("conversation-1", "Hello")

    assert response == "Fake response for: Hello"


def test_agent_chat_uses_system_prompt():
    class InspectingLLMClient(LLMClient):
        def generate(self, messages: list[dict[str, str]]) -> str:
            assert messages[0]["role"] == "system"
            assert messages[0]["content"] == (
                "You are a helpful AI assistant.\nAnswer clearly and accurately."
            )
            assert messages[1] == {
                "role": "user",
                "content": "Hello",
            }

            return "OK"

    agent = AgentService(
        llm_client=InspectingLLMClient(),
        prompt_manager=PromptManager(),
        conversation_manager=ConversationManager(),
    )

    assert agent.chat("conversation-1", "Hello") == "OK"


def test_agent_chat_preserves_conversation():
    class FakeLLMClient(LLMClient):
        def generate(self, messages: list[dict[str, str]]) -> str:
            return f"Response {len(messages)}"

    agent = AgentService(
        llm_client=FakeLLMClient(),
        prompt_manager=PromptManager(),
        conversation_manager=ConversationManager(),
    )

    first_response = agent.chat("conversation-1", "Hello")
    second_response = agent.chat("conversation-1", "How are you?")

    assert first_response == "Response 2"
    assert second_response == "Response 4"


def test_agent_chat_isolates_conversations():
    class FakeLLMClient(LLMClient):
        def generate(self, messages: list[dict[str, str]]) -> str:
            return f"Response {len(messages)}"

    agent = AgentService(
        llm_client=FakeLLMClient(),
        prompt_manager=PromptManager(),
        conversation_manager=ConversationManager(),
    )

    response_a = agent.chat("conversation-a", "Hello")
    response_b = agent.chat("conversation-b", "Hello again")

    assert response_a == "Response 2"
    assert response_b == "Response 2"
