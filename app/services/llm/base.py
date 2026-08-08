from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Interface for language model providers."""

    @abstractmethod
    def generate(self, messages: list[dict[str, str]]) -> str:
        """Generate response from LLM using conversation messages."""
        pass
