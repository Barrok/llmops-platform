from dataclasses import dataclass

from app.models.chunk import DocumentChunk


@dataclass
class Answer:
    """Represents an LLM answer and its source chunks."""

    content: str
    sources: list[DocumentChunk]
