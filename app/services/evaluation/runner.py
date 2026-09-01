from pathlib import Path

from app.services.evaluation.retrieval import recall_at_k
from app.services.retrieval.service import RetrievalService
from tests.evaluation.retrieval_dataset import RetrievalEvaluationCase


class RetrievalEvaluationRunner:
    """Runs retrieval evaluation cases and calculates Recall@K."""

    def __init__(self, retrieval_service: RetrievalService):
        self.retrieval_service = retrieval_service

    def evaluate_case(
        self,
        case: RetrievalEvaluationCase,
        k: int = 5,
    ) -> float:
        results = self.retrieval_service.retrieve(
            query=case.query,
            limit=k,
        )

        retrieved_sources = [Path(chunk.source).name for chunk in results]

        return recall_at_k(
            relevant_sources=case.relevant_sources,
            retrieved_sources=retrieved_sources,
            k=k,
        )

    def evaluate(
        self,
        cases: list[RetrievalEvaluationCase],
        k: int = 5,
    ) -> float:
        if not cases:
            return 0.0

        scores = [self.evaluate_case(case, k) for case in cases]

        return sum(scores) / len(scores)
