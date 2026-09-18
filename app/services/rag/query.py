from app.models.answer import Answer
from app.services.llm.base import LLMClient
from app.services.rag.context import ContextBuilder
from app.services.retrieval.service import RetrievalService


class RAGQueryService:
    """Application service responsible for answering RAG queries."""

    def __init__(
        self,
        llm_client: LLMClient,
        retrieval_service: RetrievalService,
        context_builder: ContextBuilder,
    ):
        self.llm_client = llm_client
        self.retrieval_service = retrieval_service
        self.context_builder = context_builder

    def answer(self, query: str, limit: int = 5) -> Answer:
        chunks = self.retrieval_service.retrieve(
            query=query,
            limit=limit,
        )

        context = self.context_builder.build(chunks)

        if context:
            prompt = f"Context:\n{context}\n\nQuestion:\n{query}"
        else:
            prompt = query

        response = self.llm_client.generate(
            [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )

        return Answer(
            content=response,
            sources=chunks,
        )
