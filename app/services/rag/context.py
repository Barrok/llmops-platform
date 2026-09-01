from app.models.chunk import DocumentChunk


class ContextBuilder:
    """Builds LLM context from retrieved document chunks."""

    def build(self, chunks: list[DocumentChunk]) -> str:
        return "\n\n".join(
            f"Source: {chunk.source}\n{chunk.content}" for chunk in chunks
        )
