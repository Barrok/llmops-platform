from app.models.document import Document


def test_document_creation():
    document = Document(
        content="Hello world",
        source="test.txt",
        metadata={
            "filename": "test.txt",
            "format": "txt",
        },
    )

    assert document.content == "Hello world"
    assert document.source == "test.txt"
    assert document.metadata == {
        "filename": "test.txt",
        "format": "txt",
    }
