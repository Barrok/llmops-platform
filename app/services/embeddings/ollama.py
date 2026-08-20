import ollama

from app.services.embeddings.base import EmbeddingClient


class OllamaEmbeddingClient(EmbeddingClient):
    """Local Ollama embedding provider."""

    def __init__(
        self,
        model: str = "nomic-embed-text",
        host: str = "http://localhost:11434",
    ):
        self.model = model
        self.client = ollama.Client(host=host)

    def embed(self, text: str) -> list[float]:
        response = self.client.embed(
            model=self.model,
            input=text,
        )

        return response["embeddings"][0]
