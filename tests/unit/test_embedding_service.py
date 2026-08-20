from unittest.mock import Mock

from app.models.chunk import DocumentChunk
from app.services.embeddings.service import EmbeddingService


def test_embed_chunk():
    client = Mock()
    client.embed.return_value = [0.1, 0.2, 0.3]

    service = EmbeddingService(client=client)

    chunk = DocumentChunk(
        content="Hello world",
        source="test.txt",
        metadata={
            "filename": "test.txt",
            "format": "txt",
            "chunk_index": "0",
        },
    )

    result = service.embed_chunk(chunk)

    client.embed.assert_called_once_with("Hello world")

    assert result.chunk == chunk
    assert result.embedding == [0.1, 0.2, 0.3]


def test_embed_chunks():
    client = Mock()
    client.embed.side_effect = [
        [0.1, 0.2],
        [0.3, 0.4],
    ]

    service = EmbeddingService(client=client)

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

    results = service.embed_chunks(chunks)

    assert len(results) == 2

    assert results[0].embedding == [0.1, 0.2]
    assert results[1].embedding == [0.3, 0.4]

    assert client.embed.call_count == 2
