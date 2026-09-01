from abc import ABC, abstractmethod

from app.models.chunk import DocumentChunk


class Retriever(ABC):
    """Abstract interface for vector retrieval."""

    @abstractmethod
    def retrieve(
        self,
        query_embedding: list[float],
        limit: int = 5,
    ) -> list[DocumentChunk]:
        """Retrieve the most relevant document chunks."""
        raise NotImplementedError
