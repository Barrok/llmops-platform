from app.models.chunk import DocumentChunk
from app.models.embedded_chunk import EmbeddedChunk
from app.services.embeddings.base import EmbeddingClient


class EmbeddingService:
    """Service responsible for generating document embeddings."""

    def __init__(self, client: EmbeddingClient):
        self.client = client

    def embed_chunk(self, chunk: DocumentChunk) -> EmbeddedChunk:
        embedding = self.client.embed(chunk.content)

        return EmbeddedChunk(
            chunk=chunk,
            embedding=embedding,
        )

    def embed_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> list[EmbeddedChunk]:
        return [self.embed_chunk(chunk) for chunk in chunks]
