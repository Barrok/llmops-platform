from abc import ABC, abstractmethod


class EmbeddingClient(ABC):
    """Interface for embedding providers."""

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Generate an embedding for a text."""
        raise NotImplementedError
