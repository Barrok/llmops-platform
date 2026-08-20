from pathlib import Path

import pytest
from pypdf import PdfWriter

from app.services.ingestion.loader import DocumentLoader


def test_load_text_document(tmp_path: Path):
    document_path = tmp_path / "test.txt"
    document_path.write_text(
        "Hello world",
        encoding="utf-8",
    )

    loader = DocumentLoader()

    document = loader.load(str(document_path))

    assert document.content == "Hello world"
    assert document.source == str(document_path)
    assert document.metadata == {
        "filename": "test.txt",
        "format": "txt",
    }


def test_load_markdown_document(tmp_path: Path):
    document_path = tmp_path / "test.md"
    document_path.write_text(
        "# Hello\n\nWorld",
        encoding="utf-8",
    )

    loader = DocumentLoader()

    document = loader.load(str(document_path))

    assert document.content == "# Hello\n\nWorld"
    assert document.metadata["format"] == "md"


def test_load_pdf_document(tmp_path: Path):
    document_path = tmp_path / "test.pdf"

    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)

    with document_path.open("wb") as file:
        writer.write(file)

    loader = DocumentLoader()

    document = loader.load(str(document_path))

    assert document.source == str(document_path)
    assert document.metadata == {
        "filename": "test.pdf",
        "format": "pdf",
    }


def test_unsupported_format():
    loader = DocumentLoader()

    with pytest.raises(ValueError, match="Unsupported document format"):
        loader.load("document.docx")
