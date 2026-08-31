import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.models.embedded_chunk import EmbeddedChunk
from app.services.vector_store.base import VectorStore


class QdrantVectorStore(VectorStore):
    """Qdrant implementation of the vector store."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        collection_name: str = "documents",
        vector_size: int = 768,
    ):
        self.collection_name = collection_name
        self.client = QdrantClient(host=host, port=port)

        self._ensure_collection(vector_size)

    def _ensure_collection(self, vector_size: int) -> None:
        collections = self.client.get_collections().collections

        if self.collection_name not in {collection.name for collection in collections}:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )

    def upsert(self, chunks: list[EmbeddedChunk]) -> None:
        points = []

        for embedded_chunk in chunks:
            chunk = embedded_chunk.chunk

            point_id = str(
                uuid.uuid5(
                    uuid.NAMESPACE_URL,
                    f"{chunk.source}:{chunk.content}",
                )
            )

            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedded_chunk.embedding,
                    payload={
                        "content": chunk.content,
                        "source": chunk.source,
                        "metadata": chunk.metadata,
                    },
                )
            )

        if points:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )
