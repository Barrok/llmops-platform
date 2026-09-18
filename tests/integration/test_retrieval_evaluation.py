import uuid
from pathlib import Path

import pytest

from app.config.settings import settings
from app.services.embeddings.ollama import OllamaEmbeddingClient
from app.services.embeddings.service import EmbeddingService
from app.services.ingestion.chunker import DocumentChunker
from app.services.ingestion.loader import DocumentLoader
from app.services.ingestion.service import DocumentIngestionService
from app.services.rag.indexing_pipeline import DocumentIndexingPipeline
from app.services.retrieval.service import RetrievalService
from app.services.vector_store.qdrant import QdrantVectorStore
from evaluation.dataset import EVALUATION_CASES
from evaluation.runner import RetrievalEvaluationRunner


@pytest.mark.integration
def test_retrieval_evaluation():
    data_path = Path("evaluation/data")
    collection_name = f"test_eval_{uuid.uuid4().hex}"

    embedding_service = EmbeddingService(
        client=OllamaEmbeddingClient(base_url=settings.OLLAMA_BASE_URL),
    )

    vector_store = QdrantVectorStore(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT,
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

    pipeline = DocumentIndexingPipeline(
        ingestion_service=ingestion_service,
        embedding_service=embedding_service,
        retrieval_service=retrieval_service,
        vector_store=vector_store,
    )

    pipeline.process_directory(str(data_path))

    runner = RetrievalEvaluationRunner(
        retrieval_service=retrieval_service,
    )

    recall = runner.evaluate(
        cases=EVALUATION_CASES,
        k=1,
    )

    assert recall >= 0.66

    vector_store.client.delete_collection(collection_name)
