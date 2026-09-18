import ollama

from app.services.embeddings.base import EmbeddingClient


class OllamaEmbeddingClient(EmbeddingClient):
    """Local Ollama embedding provider."""

    def __init__(
        self,
        base_url: str,
        model: str = "nomic-embed-text",
    ):
        self.model = model
        self.client = ollama.Client(host=base_url)

    def embed(self, text: str) -> list[float]:
        response = self.client.embed(
            model=self.model,
            input=text,
        )

        return response["embeddings"][0]
