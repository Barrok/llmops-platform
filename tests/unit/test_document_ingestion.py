from pathlib import Path

import pytest

from app.services.ingestion.chunker import DocumentChunker
from app.services.ingestion.loader import DocumentLoader
from app.services.ingestion.service import DocumentIngestionService


def test_ingest_document(tmp_path: Path):
    document_path = tmp_path / "test.txt"
    document_path.write_text(
        "Hello world",
        encoding="utf-8",
    )

    service = DocumentIngestionService(
        loader=DocumentLoader(), chunker=DocumentChunker()
    )

    document = service.ingest(str(document_path))

    assert document.content == "Hello world"
    assert document.source == str(document_path)
    assert document.metadata == {
        "filename": "test.txt",
        "format": "txt",
    }


def test_ingest_directory(tmp_path: Path):
    documents_path = tmp_path / "documents"
    documents_path.mkdir()

    first_file = documents_path / "first.txt"
    first_file.write_text(
        "First document",
        encoding="utf-8",
    )

    second_file = documents_path / "second.md"
    second_file.write_text(
        "# Second document",
        encoding="utf-8",
    )

    unsupported_file = documents_path / "ignored.docx"
    unsupported_file.write_text(
        "Should be ignored",
        encoding="utf-8",
    )

    service = DocumentIngestionService(
        loader=DocumentLoader(), chunker=DocumentChunker()
    )

    documents = service.ingest_directory(
        str(documents_path),
    )

    assert len(documents) == 2

    assert {document.metadata["filename"] for document in documents} == {
        "first.txt",
        "second.md",
    }


def test_ingest_empty_directory(tmp_path: Path):
    documents_path = tmp_path / "documents"
    documents_path.mkdir()

    service = DocumentIngestionService(
        loader=DocumentLoader(), chunker=DocumentChunker()
    )

    documents = service.ingest_directory(
        str(documents_path),
    )

    assert documents == []


def test_ingest_directory_requires_directory(tmp_path: Path):
    file_path = tmp_path / "file.txt"
    file_path.write_text(
        "Not a directory",
        encoding="utf-8",
    )

    service = DocumentIngestionService(
        loader=DocumentLoader(), chunker=DocumentChunker()
    )

    with pytest.raises(ValueError, match="Not a directory"):
        service.ingest_directory(str(file_path))


def test_ingest_and_chunk(tmp_path: Path):
    document_path = tmp_path / "test.txt"
    document_path.write_text(
        "A" * 1500,
        encoding="utf-8",
    )

    service = DocumentIngestionService(
        loader=DocumentLoader(),
        chunker=DocumentChunker(
            chunk_size=1000,
            chunk_overlap=200,
        ),
    )

    chunks = service.ingest_and_chunk(
        str(document_path),
    )

    assert len(chunks) == 2
    assert chunks[0].source == str(document_path)
    assert chunks[0].metadata["chunk_index"] == "0"
    assert chunks[1].metadata["chunk_index"] == "1"


def test_ingest_and_chunk_directory(tmp_path: Path):
    documents_path = tmp_path / "documents"
    documents_path.mkdir()

    first_file = documents_path / "first.txt"
    first_file.write_text(
        "A" * 1500,
        encoding="utf-8",
    )

    second_file = documents_path / "second.md"
    second_file.write_text(
        "B" * 1500,
        encoding="utf-8",
    )

    service = DocumentIngestionService(
        loader=DocumentLoader(),
        chunker=DocumentChunker(
            chunk_size=1000,
            chunk_overlap=200,
        ),
    )

    chunks = service.ingest_and_chunk_directory(
        str(documents_path),
    )

    assert len(chunks) == 4

    assert {chunk.metadata["filename"] for chunk in chunks} == {
        "first.txt",
        "second.md",
    }

    assert chunks[0].metadata["chunk_index"] == "0"
    assert chunks[1].metadata["chunk_index"] == "1"
    assert chunks[2].metadata["chunk_index"] == "0"
    assert chunks[3].metadata["chunk_index"] == "1"
