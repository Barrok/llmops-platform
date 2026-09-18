import math
import uuid

import pytest

from app.config.settings import settings
from app.models.chunk import DocumentChunk
from app.models.embedded_chunk import EmbeddedChunk
from app.services.vector_store.qdrant import QdrantVectorStore


@pytest.mark.integration
def test_qdrant_vector_store_upsert():
    collection_name = f"test_documents_{uuid.uuid4().hex}"

    store = QdrantVectorStore(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT,
        collection_name=collection_name,
        vector_size=768,
    )

    chunk = DocumentChunk(
        content="Hello world",
        source="test.txt",
        metadata={"format": "txt"},
    )

    embedded_chunk = EmbeddedChunk(
        chunk=chunk,
        embedding=[0.1] * 768,
    )

    store.upsert([embedded_chunk])

    points, _ = store.client.scroll(
        collection_name=collection_name,
        limit=10,
        with_payload=True,
        with_vectors=True,
    )

    assert len(points) == 1

    expected_value = 1 / math.sqrt(768)

    assert len(points[0].vector) == 768
    assert all(
        math.isclose(value, expected_value, rel_tol=1e-6) for value in points[0].vector
    )

    assert points[0].payload == {
        "content": "Hello world",
        "source": "test.txt",
        "metadata": {"format": "txt"},
    }

    store.client.delete_collection(collection_name)
