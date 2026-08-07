class PromptManager:
    """Manages system prompts and prompt templates."""

    DEFAULT_SYSTEM_PROMPT = """
You are a helpful AI assistant.
Answer clearly and accurately.
"""

    def get_system_prompt(self) -> str:
        return self.DEFAULT_SYSTEM_PROMPT.strip()
