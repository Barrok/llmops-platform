from abc import ABC, abstractmethod

from app.models.embedded_chunk import EmbeddedChunk


class VectorStore(ABC):
    """Abstract interface for vector storage."""

    @abstractmethod
    def upsert(self, chunks: list[EmbeddedChunk]) -> None:
        """Store embedded chunks."""
        raise NotImplementedError
