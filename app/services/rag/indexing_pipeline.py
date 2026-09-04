from app.models.chunk import DocumentChunk
from app.models.embedded_chunk import EmbeddedChunk
from app.services.embeddings.service import EmbeddingService
from app.services.ingestion.service import DocumentIngestionService
from app.services.retrieval.service import RetrievalService
from app.services.vector_store.base import VectorStore


class DocumentIndexingPipeline:
    """Orchestrates document processing and retrieval."""

    def __init__(
        self,
        ingestion_service: DocumentIngestionService,
        embedding_service: EmbeddingService,
        retrieval_service: RetrievalService,
        vector_store: VectorStore,
    ):
        self.ingestion_service = ingestion_service
        self.embedding_service = embedding_service
        self.retrieval_service = retrieval_service
        self.vector_store = vector_store

    def process_directory(
        self,
        path: str,
    ) -> list[EmbeddedChunk]:
        chunks = self.ingestion_service.ingest_and_chunk_directory(
            path,
        )

        embedded_chunks = self.embedding_service.embed_chunks(chunks)

        self.vector_store.upsert(embedded_chunks)

        return embedded_chunks

    def retrieve(
        self,
        query: str,
        limit: int = 5,
    ) -> list[DocumentChunk]:
        return self.retrieval_service.retrieve(
            query=query,
            limit=limit,
        )
