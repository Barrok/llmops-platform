from app.services.vector_store.retriever import Retriever


def test_retriever_is_abstract():
    assert Retriever.__abstractmethods__ == {"retrieve"}
