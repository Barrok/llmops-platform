from app.models.chunk import DocumentChunk
from app.models.embedded_chunk import EmbeddedChunk


def test_embedded_chunk_creation():
    chunk = DocumentChunk(
        content="Hello world",
        source="test.txt",
        metadata={
            "filename": "test.txt",
            "format": "txt",
            "chunk_index": "0",
        },
    )

    embedded_chunk = EmbeddedChunk(
        chunk=chunk,
        embedding=[0.1, 0.2, 0.3],
    )

    assert embedded_chunk.chunk == chunk
    assert embedded_chunk.embedding == [0.1, 0.2, 0.3]
