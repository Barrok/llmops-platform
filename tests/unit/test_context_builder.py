from app.models.chunk import DocumentChunk
from app.services.rag.context import ContextBuilder


def test_context_builder_builds_context():
    chunks = [
        DocumentChunk(
            content="Python is a programming language.",
            source="python.txt",
            metadata={"format": "txt"},
        ),
        DocumentChunk(
            content="Python is widely used in machine learning.",
            source="python.txt",
            metadata={"format": "txt"},
        ),
    ]

    builder = ContextBuilder()

    result = builder.build(chunks)

    assert result == (
        "Source: python.txt\n"
        "Python is a programming language.\n\n"
        "Source: python.txt\n"
        "Python is widely used in machine learning."
    )
