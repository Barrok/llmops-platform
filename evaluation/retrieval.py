def recall_at_k(
    relevant_sources: set[str],
    retrieved_sources: list[str],
    k: int,
) -> float:
    """Calculate Recall@K for retrieved document sources."""

    if not relevant_sources:
        return 0.0

    retrieved_at_k = set(retrieved_sources[:k])

    relevant_retrieved = relevant_sources & retrieved_at_k

    return len(relevant_retrieved) / len(relevant_sources)
