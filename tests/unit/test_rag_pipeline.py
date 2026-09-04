from unittest.mock import Mock

from app.models.chunk import DocumentChunk
from app.models.embedded_chunk import EmbeddedChunk
from app.services.rag.indexing_pipeline import DocumentIndexingPipeline


def test_process_directory():
    ingestion_service = Mock()
    embedding_service = Mock()
    retrieval_service = Mock()
    vector_store = Mock()

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

    pipeline = DocumentIndexingPipeline(
        ingestion_service=ingestion_service,
        embedding_service=embedding_service,
        retrieval_service=retrieval_service,
        vector_store=vector_store,
    )

    result = pipeline.process_directory("data/documents")

    ingestion_service.ingest_and_chunk_directory.assert_called_once_with(
        "data/documents",
    )

    embedding_service.embed_chunks.assert_called_once_with(
        chunks,
    )

    vector_store.upsert.assert_called_once_with(
        embedded_chunks,
    )

    assert result == embedded_chunks


def test_retrieve():
    ingestion_service = Mock()
    embedding_service = Mock()
    retrieval_service = Mock()
    vector_store = Mock()

    expected_chunks = [
        DocumentChunk(
            content="Python is a programming language.",
            source="python.txt",
            metadata={"format": "txt"},
        ),
    ]

    retrieval_service.retrieve.return_value = expected_chunks

    pipeline = DocumentIndexingPipeline(
        ingestion_service=ingestion_service,
        embedding_service=embedding_service,
        retrieval_service=retrieval_service,
        vector_store=vector_store,
    )

    result = pipeline.retrieve(
        query="What is Python?",
        limit=3,
    )

    retrieval_service.retrieve.assert_called_once_with(
        query="What is Python?",
        limit=3,
    )

    assert result == expected_chunks
