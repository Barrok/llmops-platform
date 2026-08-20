from app.models.chunk import DocumentChunk


def test_document_chunk_creation():
    chunk = DocumentChunk(
        content="Hello world",
        source="test.txt",
        metadata={
            "filename": "test.txt",
            "format": "txt",
            "chunk_index": "0",
        },
    )

    assert chunk.content == "Hello world"
    assert chunk.source == "test.txt"
    assert chunk.metadata == {
        "filename": "test.txt",
        "format": "txt",
        "chunk_index": "0",
    }
