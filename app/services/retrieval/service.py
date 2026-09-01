from app.models.chunk import DocumentChunk
from app.services.embeddings.service import EmbeddingService
from app.services.vector_store.retriever import Retriever


class RetrievalService:
    """Application service responsible for document retrieval."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        retriever: Retriever,
    ):
        self.embedding_service = embedding_service
        self.retriever = retriever

    def retrieve(
        self,
        query: str,
        limit: int = 5,
    ) -> list[DocumentChunk]:
        """Embed a query and retrieve relevant document chunks."""
        query_embedding = self.embedding_service.embed_query(query)

        return self.retriever.retrieve(
            query_embedding=query_embedding,
            limit=limit,
        )
