from app.models.embedded_chunk import EmbeddedChunk
from app.services.embeddings.service import EmbeddingService
from app.services.ingestion.service import DocumentIngestionService


class RAGPipeline:
    """Orchestrates document ingestion, chunking and embedding."""

    def __init__(
        self,
        ingestion_service: DocumentIngestionService,
        embedding_service: EmbeddingService,
    ):
        self.ingestion_service = ingestion_service
        self.embedding_service = embedding_service

    def process_directory(
        self,
        path: str,
    ) -> list[EmbeddedChunk]:
        chunks = self.ingestion_service.ingest_and_chunk_directory(
            path,
        )

        return self.embedding_service.embed_chunks(chunks)
