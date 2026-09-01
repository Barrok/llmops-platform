from app.services.evaluation.retrieval import recall_at_k


def test_recall_at_k_all_relevant_found():
    relevant = {"a.txt", "b.txt"}

    retrieved = [
        "a.txt",
        "b.txt",
        "c.txt",
    ]

    assert recall_at_k(relevant, retrieved, 3) == 1.0


def test_recall_at_k_partially_relevant():
    relevant = {"a.txt", "b.txt"}

    retrieved = [
        "a.txt",
        "c.txt",
        "d.txt",
    ]

    assert recall_at_k(relevant, retrieved, 3) == 0.5


def test_recall_at_k_none_relevant():
    relevant = {"a.txt", "b.txt"}

    retrieved = [
        "c.txt",
        "d.txt",
    ]

    assert recall_at_k(relevant, retrieved, 2) == 0.0


def test_recall_at_k_respects_k():
    relevant = {"a.txt", "b.txt"}

    retrieved = [
        "a.txt",
        "c.txt",
        "b.txt",
    ]

    assert recall_at_k(relevant, retrieved, 2) == 0.5


def test_recall_at_k_empty_relevant():
    assert recall_at_k(set(), ["a.txt"], 1) == 0.0
