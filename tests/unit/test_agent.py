from unittest.mock import Mock

from app.models.chunk import DocumentChunk
from app.services.agent.conversation import ConversationManager
from app.services.agent.prompts import PromptManager
from app.services.agent.service import AgentService
from app.services.llm.base import LLMClient
from app.services.rag.context import ContextBuilder


class FakeLLMClient(LLMClient):
    def generate(self, messages: list[dict[str, str]]) -> str:
        return f"Fake response for: {messages[-1]['content']}"


def test_agent_chat():
    retrieval_service = Mock()
    retrieval_service.retrieve.return_value = []

    agent = AgentService(
        llm_client=FakeLLMClient(),
        prompt_manager=PromptManager(),
        conversation_manager=ConversationManager(),
        retrieval_service=retrieval_service,
        context_builder=ContextBuilder(),
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

    retrieval_service = Mock()
    retrieval_service.retrieve.return_value = []

    agent = AgentService(
        llm_client=InspectingLLMClient(),
        prompt_manager=PromptManager(),
        conversation_manager=ConversationManager(),
        retrieval_service=retrieval_service,
        context_builder=ContextBuilder(),
    )

    assert agent.chat("conversation-1", "Hello") == "OK"


def test_agent_chat_preserves_conversation():
    class FakeLLMClient(LLMClient):
        def generate(self, messages: list[dict[str, str]]) -> str:
            return f"Response {len(messages)}"

    retrieval_service = Mock()
    retrieval_service.retrieve.return_value = []

    agent = AgentService(
        llm_client=FakeLLMClient(),
        prompt_manager=PromptManager(),
        conversation_manager=ConversationManager(),
        retrieval_service=retrieval_service,
        context_builder=ContextBuilder(),
    )

    first_response = agent.chat("conversation-1", "Hello")
    second_response = agent.chat("conversation-1", "How are you?")

    assert first_response == "Response 2"
    assert second_response == "Response 4"


def test_agent_chat_isolates_conversations():
    class FakeLLMClient(LLMClient):
        def generate(self, messages: list[dict[str, str]]) -> str:
            return f"Response {len(messages)}"

    retrieval_service = Mock()
    retrieval_service.retrieve.return_value = []

    agent = AgentService(
        llm_client=FakeLLMClient(),
        prompt_manager=PromptManager(),
        conversation_manager=ConversationManager(),
        retrieval_service=retrieval_service,
        context_builder=ContextBuilder(),
    )

    response_a = agent.chat("conversation-a", "Hello")
    response_b = agent.chat("conversation-b", "Hello again")

    assert response_a == "Response 2"
    assert response_b == "Response 2"


def test_agent_retrieve_context():
    retrieval_service = Mock()

    retrieved_chunks = [
        DocumentChunk(
            content="Python is a programming language.",
            source="python.txt",
            metadata={"format": "txt"},
        ),
        DocumentChunk(
            content="Python is widely used for machine learning.",
            source="python.txt",
            metadata={"format": "txt"},
        ),
    ]

    retrieval_service.retrieve.return_value = retrieved_chunks

    agent = AgentService(
        llm_client=FakeLLMClient(),
        prompt_manager=PromptManager(),
        conversation_manager=ConversationManager(),
        retrieval_service=retrieval_service,
        context_builder=ContextBuilder(),
    )

    result = agent.retrieve_context(
        query="What is Python?",
        limit=2,
    )

    retrieval_service.retrieve.assert_called_once_with(
        query="What is Python?",
        limit=2,
    )

    assert result == retrieved_chunks


def test_agent_chat_injects_retrieved_context():
    retrieval_service = Mock()

    retrieval_service.retrieve.return_value = [
        DocumentChunk(
            content="Python is a programming language.",
            source="python.txt",
            metadata={"format": "txt"},
        ),
    ]

    class InspectingLLMClient(LLMClient):
        def generate(self, messages: list[dict[str, str]]) -> str:
            assert messages[0]["role"] == "system"

            assert messages[1]["role"] == "user"
            assert messages[1]["content"] == (
                "Context:\n"
                "Source: python.txt\n"
                "Python is a programming language.\n\n"
                "Question:\n"
                "What is Python?"
            )

            return "Python is a programming language."

    agent = AgentService(
        llm_client=InspectingLLMClient(),
        prompt_manager=PromptManager(),
        conversation_manager=ConversationManager(),
        retrieval_service=retrieval_service,
        context_builder=ContextBuilder(),
    )

    response = agent.chat(
        "conversation-1",
        "What is Python?",
    )

    retrieval_service.retrieve.assert_called_once_with(
        query="What is Python?",
        limit=5,
    )

    assert response == "Python is a programming language."
