from app.services.vector_store.base import VectorStore


def test_vector_store_is_abstract():
    assert VectorStore.__abstractmethods__ == {"upsert"}
