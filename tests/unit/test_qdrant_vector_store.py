from unittest.mock import MagicMock, patch

from app.models.chunk import DocumentChunk
from app.models.embedded_chunk import EmbeddedChunk
from app.services.vector_store.qdrant import QdrantVectorStore


@patch("app.services.vector_store.qdrant.QdrantClient")
def test_qdrant_vector_store_creates_collection(mock_client):
    mock_instance = MagicMock()
    mock_instance.get_collections.return_value.collections = []
    mock_client.return_value = mock_instance

    QdrantVectorStore()

    mock_client.assert_called_once_with(
        host="localhost",
        port=6333,
    )

    mock_instance.create_collection.assert_called_once()

    call_kwargs = mock_instance.create_collection.call_args.kwargs

    assert call_kwargs["collection_name"] == "documents"

    vector_config = call_kwargs["vectors_config"]

    assert vector_config.size == 768
    assert vector_config.distance.value == "Cosine"


@patch("app.services.vector_store.qdrant.QdrantClient")
def test_qdrant_vector_store_upserts_chunks(mock_client):
    mock_instance = MagicMock()
    mock_instance.get_collections.return_value.collections = []

    mock_client.return_value = mock_instance

    store = QdrantVectorStore()

    chunk = DocumentChunk(
        content="Hello world",
        source="test.txt",
        metadata={"format": "txt"},
    )

    embedded_chunk = EmbeddedChunk(
        chunk=chunk,
        embedding=[0.1, 0.2, 0.3],
    )

    store.upsert([embedded_chunk])

    mock_instance.upsert.assert_called_once()

    call_kwargs = mock_instance.upsert.call_args.kwargs

    assert call_kwargs["collection_name"] == "documents"

    points = call_kwargs["points"]

    assert len(points) == 1
    assert points[0].vector == [0.1, 0.2, 0.3]
    assert points[0].payload == {
        "content": "Hello world",
        "source": "test.txt",
        "metadata": {"format": "txt"},
    }
