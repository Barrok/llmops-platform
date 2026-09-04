from abc import ABC, abstractmethod

from app.models.chunk import DocumentChunk
from app.models.document import Document


class ChunkerPort(ABC):
    """Abstract interface for document chunking."""

    @abstractmethod
    def chunk(self, document: Document) -> list[DocumentChunk]:
        """Split a document into chunks."""
        raise NotImplementedError
