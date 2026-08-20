from app.models.document import Document
from app.services.ingestion.chunker import DocumentChunker


def test_document_is_split_into_chunks():
    document = Document(
        content="A" * 2500,
        source="test.txt",
        metadata={
            "filename": "test.txt",
            "format": "txt",
        },
    )

    chunker = DocumentChunker(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = chunker.chunk(document)

    assert len(chunks) == 3

    assert chunks[0].content == "A" * 1000
    assert chunks[1].content == "A" * 1000
    assert chunks[2].content == "A" * 900


def test_chunks_preserve_document_metadata():
    document = Document(
        content="Hello world",
        source="test.md",
        metadata={
            "filename": "test.md",
            "format": "md",
        },
    )

    chunker = DocumentChunker()

    chunks = chunker.chunk(document)

    assert chunks[0].source == "test.md"
    assert chunks[0].metadata == {
        "filename": "test.md",
        "format": "md",
        "chunk_index": "0",
    }


def test_chunks_overlap():
    document = Document(
        content="A" * 1500,
        source="test.txt",
        metadata={
            "filename": "test.txt",
            "format": "txt",
        },
    )

    chunker = DocumentChunker(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = chunker.chunk(document)

    assert len(chunks) == 2
    assert chunks[0].content[-200:] == chunks[1].content[:200]
