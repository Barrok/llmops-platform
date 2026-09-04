from evaluation.dataset import EVALUATION_CASES


def test_retrieval_evaluation_dataset():
    assert EVALUATION_CASES

    for case in EVALUATION_CASES:
        assert case.query
        assert case.relevant_sources
