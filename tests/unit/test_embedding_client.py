from app.services.embeddings.base import EmbeddingClient


def test_embedding_client_is_abstract():
    assert EmbeddingClient.__abstractmethods__ == {"embed"}
