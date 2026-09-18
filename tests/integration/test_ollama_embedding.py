import pytest

from app.config.settings import settings
from app.services.embeddings.ollama import OllamaEmbeddingClient


@pytest.mark.integration
def test_ollama_embedding():
    client = OllamaEmbeddingClient(base_url=settings.OLLAMA_BASE_URL)

    embedding = client.embed("Hello world")

    assert isinstance(embedding, list)
    assert len(embedding) > 0
    assert all(isinstance(value, float) for value in embedding)
