from unittest.mock import Mock

from app.models.chunk import DocumentChunk
from app.models.embedded_chunk import EmbeddedChunk
from app.services.rag.pipeline import RAGPipeline


def test_process_directory():
    ingestion_service = Mock()
    embedding_service = Mock()

    chunks = [
        DocumentChunk(
            content="First chunk",
            source="test.txt",
            metadata={"chunk_index": "0"},
        ),
        DocumentChunk(
            content="Second chunk",
            source="test.txt",
            metadata={"chunk_index": "1"},
        ),
    ]

    embedded_chunks = [
        EmbeddedChunk(
            chunk=chunks[0],
            embedding=[0.1, 0.2],
        ),
        EmbeddedChunk(
            chunk=chunks[1],
            embedding=[0.3, 0.4],
        ),
    ]

    ingestion_service.ingest_and_chunk_directory.return_value = chunks
    embedding_service.embed_chunks.return_value = embedded_chunks

    pipeline = RAGPipeline(
        ingestion_service=ingestion_service,
        embedding_service=embedding_service,
    )

    result = pipeline.process_directory("data/documents")

    ingestion_service.ingest_and_chunk_directory.assert_called_once_with(
        "data/documents",
    )

    embedding_service.embed_chunks.assert_called_once_with(
        chunks,
    )

    assert result == embedded_chunks
