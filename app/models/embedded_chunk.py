from dataclasses import dataclass

from app.models.chunk import DocumentChunk


@dataclass
class EmbeddedChunk:
    chunk: DocumentChunk
    embedding: list[float]
