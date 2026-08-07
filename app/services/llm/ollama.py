import ollama

from app.services.llm.base import LLMClient


class OllamaClient(LLMClient):
    """Local Ollama LLM provider."""

    def __init__(self, model: str = "qwen3:8b"):
        self.model = model

    def generate(self, prompt: str) -> str:
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]
