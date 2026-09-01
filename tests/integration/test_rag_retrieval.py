import uuid
from pathlib import Path

import pytest

from app.services.embeddings.ollama import OllamaEmbeddingClient
from app.services.embeddings.service import EmbeddingService
from app.services.ingestion.chunker import DocumentChunker
from app.services.ingestion.loader import DocumentLoader
from app.services.ingestion.service import DocumentIngestionService
from app.services.rag.pipeline import RAGPipeline
from app.services.retrieval.service import RetrievalService
from app.services.vector_store.qdrant import QdrantVectorStore


@pytest.mark.integration
def test_rag_pipeline_indexes_and_retrieves(tmp_path: Path):
    document_path = tmp_path / "python.txt"

    document_path.write_text(
        "Python is a programming language.",
        encoding="utf-8",
    )

    collection_name = f"test_rag_{uuid.uuid4().hex}"

    embedding_service = EmbeddingService(
        client=OllamaEmbeddingClient(),
    )

    vector_store = QdrantVectorStore(
        host="localhost",
        port=6333,
        collection_name=collection_name,
        vector_size=768,
    )

    ingestion_service = DocumentIngestionService(
        loader=DocumentLoader(),
        chunker=DocumentChunker(),
    )

    retrieval_service = RetrievalService(
        embedding_service=embedding_service,
        retriever=vector_store,
    )

    pipeline = RAGPipeline(
        ingestion_service=ingestion_service,
        embedding_service=embedding_service,
        retrieval_service=retrieval_service,
        vector_store=vector_store,
    )

    pipeline.process_directory(str(tmp_path))

    results = pipeline.retrieve(
        query="What is Python?",
        limit=1,
    )

    assert len(results) == 1
    assert results[0].content == "Python is a programming language."

    vector_store.client.delete_collection(collection_name)
