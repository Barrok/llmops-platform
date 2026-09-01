from unittest.mock import Mock

from app.models.chunk import DocumentChunk
from app.services.evaluation.runner import RetrievalEvaluationRunner
from tests.evaluation.retrieval_dataset import RetrievalEvaluationCase


def test_evaluate_case():
    retrieval_service = Mock()

    retrieval_service.retrieve.return_value = [
        DocumentChunk(
            content="Python is a programming language.",
            source="python.txt",
            metadata={},
        ),
        DocumentChunk(
            content="Some unrelated content.",
            source="other.txt",
            metadata={},
        ),
    ]

    case = RetrievalEvaluationCase(
        query="What is Python?",
        relevant_sources={"python.txt"},
    )

    runner = RetrievalEvaluationRunner(
        retrieval_service=retrieval_service,
    )

    result = runner.evaluate_case(case, k=2)

    retrieval_service.retrieve.assert_called_once_with(
        query="What is Python?",
        limit=2,
    )

    assert result == 1.0


def test_evaluate():
    retrieval_service = Mock()

    retrieval_service.retrieve.side_effect = [
        [
            DocumentChunk(
                content="Python",
                source="python.txt",
                metadata={},
            ),
        ],
        [
            DocumentChunk(
                content="Paris",
                source="geography.txt",
                metadata={},
            ),
        ],
    ]

    cases = [
        RetrievalEvaluationCase(
            query="What is Python?",
            relevant_sources={"python.txt"},
        ),
        RetrievalEvaluationCase(
            query="What is the capital of France?",
            relevant_sources={"geography.txt"},
        ),
    ]

    runner = RetrievalEvaluationRunner(
        retrieval_service=retrieval_service,
    )

    result = runner.evaluate(cases, k=1)

    assert result == 1.0
    assert retrieval_service.retrieve.call_count == 2


def test_evaluate_case_normalizes_source_path():
    retrieval_service = Mock()

    retrieval_service.retrieve.return_value = [
        DocumentChunk(
            content="Python is a programming language.",
            source="tests/evaluation/data/python.txt",
            metadata={},
        ),
    ]

    case = RetrievalEvaluationCase(
        query="What is Python?",
        relevant_sources={"python.txt"},
    )

    runner = RetrievalEvaluationRunner(
        retrieval_service=retrieval_service,
    )

    result = runner.evaluate_case(case, k=1)

    assert result == 1.0
