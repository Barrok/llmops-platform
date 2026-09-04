import uuid
from pathlib import Path

import pytest

from app.services.agent.conversation import ConversationManager
from app.services.agent.prompts import PromptManager
from app.services.agent.service import AgentService
from app.services.embeddings.ollama import OllamaEmbeddingClient
from app.services.embeddings.service import EmbeddingService
from app.services.ingestion.chunker import DocumentChunker
from app.services.ingestion.loader import DocumentLoader
from app.services.ingestion.service import DocumentIngestionService
from app.services.llm.ollama import OllamaClient
from app.services.rag.context import ContextBuilder
from app.services.rag.indexing_pipeline import DocumentIndexingPipeline
from app.services.retrieval.service import RetrievalService
from app.services.vector_store.qdrant import QdrantVectorStore


@pytest.mark.integration
def test_rag_end_to_end():
    data_path = Path("evaluation/data")

    collection_name = f"test_e2e_{uuid.uuid4().hex}"

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

    agent = AgentService(
        llm_client=OllamaClient(),
        prompt_manager=PromptManager(),
        conversation_manager=ConversationManager(),
        retrieval_service=retrieval_service,
        context_builder=ContextBuilder(),
    )

    retrieved_chunks = retrieval_service.retrieve(
        query="What is Python?",
        limit=1,
    )

    assert retrieved_chunks
    assert retrieved_chunks[0].source.endswith("python.txt")

    response = agent.chat(
        conversation_id="e2e-test",
        message="What is Python?",
    )

    assert response
