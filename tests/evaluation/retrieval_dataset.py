from dataclasses import dataclass


@dataclass
class RetrievalEvaluationCase:
    query: str
    relevant_sources: set[str]


EVALUATION_CASES = [
    RetrievalEvaluationCase(
        query="What is Python?",
        relevant_sources={"python.txt"},
    ),
    RetrievalEvaluationCase(
        query="What is the capital of France?",
        relevant_sources={"geography.txt"},
    ),
    RetrievalEvaluationCase(
        query="How does Docker isolate applications?",
        relevant_sources={"docker.txt"},
    ),
]
