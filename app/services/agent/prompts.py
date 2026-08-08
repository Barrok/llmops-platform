class PromptManager:
    """Manage system prompts and prompt construction."""

    DEFAULT_SYSTEM_PROMPT = """
You are a helpful AI assistant.
Answer clearly and accurately.
"""

    def __init__(self, system_prompt: str | None = None) -> None:
        self._system_prompt = (
            system_prompt.strip()
            if system_prompt is not None
            else self.DEFAULT_SYSTEM_PROMPT.strip()
        )

    def get_system_prompt(self) -> str:
        return self._system_prompt

    def build_messages(self, user_message: str) -> list[dict[str, str]]:
        return [
            {
                "role": "system",
                "content": self.get_system_prompt(),
            },
            {
                "role": "user",
                "content": user_message,
            },
        ]
