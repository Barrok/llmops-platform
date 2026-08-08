from enum import StrEnum


class MessageRole(StrEnum):
    """Supported conversation message roles."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ConversationManager:
    """Manage multiple conversation histories."""

    def __init__(self) -> None:
        self._conversations: dict[str, list[dict[str, str]]] = {}

    def add_message(
        self,
        conversation_id: str,
        role: MessageRole,
        content: str,
    ) -> None:
        self._conversations.setdefault(conversation_id, []).append(
            {
                "role": role.value,
                "content": content,
            }
        )

    def get_messages(
        self,
        conversation_id: str,
    ) -> list[dict[str, str]]:
        return self._conversations.get(conversation_id, []).copy()

    def clear(self, conversation_id: str) -> None:
        self._conversations.pop(conversation_id, None)
