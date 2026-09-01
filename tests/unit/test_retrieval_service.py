from unittest.mock import Mock

from app.models.chunk import DocumentChunk
from app.services.retrieval.service import RetrievalService


def test_retrieval_service():
    embedding_service = Mock()
    retriever = Mock()

    embedding_service.embed_query.return_value = [0.1, 0.2, 0.3]

    expected_chunks = [
        DocumentChunk(
            content="Python is a programming language.",
            source="python.txt",
            metadata={"format": "txt"},
        ),
    ]

    retriever.retrieve.return_value = expected_chunks

    service = RetrievalService(
        embedding_service=embedding_service,
        retriever=retriever,
    )

    result = service.retrieve(
        query="What is Python?",
        limit=3,
    )

    embedding_service.embed_query.assert_called_once_with("What is Python?")

    retriever.retrieve.assert_called_once_with(
        query_embedding=[0.1, 0.2, 0.3],
        limit=3,
    )

    assert result == expected_chunks
