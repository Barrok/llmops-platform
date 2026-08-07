from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Interface for language model providers."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate response from LLM."""
        pass
