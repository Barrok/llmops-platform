from unittest.mock import patch

from app.services.embeddings.ollama import OllamaEmbeddingClient


def test_ollama_embedding_client():
    response = {
        "embeddings": [
            [0.1, 0.2, 0.3],
        ],
    }

    with patch("app.services.embeddings.ollama.ollama.Client") as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.embed.return_value = response

        client = OllamaEmbeddingClient()

        embedding = client.embed("Hello world")

    mock_client.assert_called_once_with(
        host="http://localhost:11434",
    )

    mock_instance.embed.assert_called_once_with(
        model="nomic-embed-text",
        input="Hello world",
    )

    assert embedding == [0.1, 0.2, 0.3]
