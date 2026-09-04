import uuid
from pathlib import Path

import pytest

from app.services.embeddings.ollama import OllamaEmbeddingClient
from app.services.embeddings.service import EmbeddingService
from app.services.evaluation.runner import RetrievalEvaluationRunner
from app.services.ingestion.chunker import DocumentChunker
from app.services.ingestion.loader import DocumentLoader
from app.services.ingestion.service import DocumentIngestionService
from app.services.rag.indexing_pipeline import DocumentIndexingPipeline
from app.services.retrieval.service import RetrievalService
from app.services.vector_store.qdrant import QdrantVectorStore
from tests.evaluation.retrieval_dataset import EVALUATION_CASES


@pytest.mark.integration
def test_retrieval_evaluation():
    data_path = Path("tests/evaluation/data")
    collection_name = f"test_eval_{uuid.uuid4().hex}"

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

    recall = runner.evaluate(
        cases=EVALUATION_CASES,
        k=1,
    )

    assert recall >= 0.66

    vector_store.client.delete_collection(collection_name)
