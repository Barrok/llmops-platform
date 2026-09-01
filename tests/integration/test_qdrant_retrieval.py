import uuid

import pytest

from app.models.chunk import DocumentChunk
from app.models.embedded_chunk import EmbeddedChunk
from app.services.vector_store.qdrant import QdrantVectorStore


@pytest.mark.integration
def test_qdrant_retrieves_most_similar_chunk():
    collection_name = f"test_retrieval_{uuid.uuid4().hex}"

    store = QdrantVectorStore(
        host="localhost",
        port=6333,
        collection_name=collection_name,
        vector_size=3,
    )

    chunks = [
        EmbeddedChunk(
            chunk=DocumentChunk(
                content="Python is a programming language.",
                source="python.txt",
                metadata={"format": "txt"},
            ),
            embedding=[1.0, 0.0, 0.0],
        ),
        EmbeddedChunk(
            chunk=DocumentChunk(
                content="The capital of France is Paris.",
                source="geography.txt",
                metadata={"format": "txt"},
            ),
            embedding=[0.0, 1.0, 0.0],
        ),
        EmbeddedChunk(
            chunk=DocumentChunk(
                content="Python supports object-oriented programming.",
                source="python.txt",
                metadata={"format": "txt"},
            ),
            embedding=[0.9, 0.1, 0.0],
        ),
    ]

    store.upsert(chunks)

    results = store.retrieve(
        query_embedding=[1.0, 0.0, 0.0],
        limit=2,
    )

    assert len(results) == 2

    assert results[0].content == "Python is a programming language."
    assert results[1].content == ("Python supports object-oriented programming.")

    store.client.delete_collection(collection_name)
