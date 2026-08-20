import pytest

from app.services.embeddings.ollama import OllamaEmbeddingClient


@pytest.mark.integration
def test_ollama_embedding():
    client = OllamaEmbeddingClient()

    embedding = client.embed("Hello world")

    assert isinstance(embedding, list)
    assert len(embedding) > 0
    assert all(isinstance(value, float) for value in embedding)
