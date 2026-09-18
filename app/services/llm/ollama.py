import ollama

from app.services.llm.base import LLMClient


class OllamaClient(LLMClient):
    """Local Ollama LLM provider."""

    def __init__(self, base_url: str, model: str = "qwen3:8b") -> None:
        self.model = model
        self.client = ollama.Client(host=base_url)

    def generate(self, messages: list[dict[str, str]]) -> str:
        response = self.client.chat(
            model=self.model,
            messages=messages,
        )

        return response["message"]["content"]
