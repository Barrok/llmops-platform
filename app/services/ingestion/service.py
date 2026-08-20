from pathlib import Path

from app.models.chunk import DocumentChunk
from app.models.document import Document
from app.services.ingestion.chunker import DocumentChunker
from app.services.ingestion.loader import DocumentLoader


class DocumentIngestionService:
    """Service responsible for document ingestion."""

    def __init__(
        self,
        loader: DocumentLoader,
        chunker: DocumentChunker,
    ):
        self.loader = loader
        self.chunker = chunker

    def ingest(self, path: str) -> Document:
        return self.loader.load(path)

    def ingest_directory(self, path: str) -> list[Document]:
        directory = Path(path)

        if not directory.is_dir():
            raise ValueError(f"Not a directory: {path}")

        documents = []

        for file_path in directory.iterdir():
            if file_path.is_file() and (
                file_path.suffix.lower() in self.loader.SUPPORTED_FORMATS
            ):
                documents.append(self.loader.load(str(file_path)))

        return documents

    def ingest_and_chunk(self, path: str) -> list[DocumentChunk]:
        document = self.ingest(path)

        return self.chunker.chunk(document)

    def ingest_and_chunk_directory(
        self,
        path: str,
    ) -> list[DocumentChunk]:
        documents = self.ingest_directory(path)

        chunks = []

        for document in documents:
            chunks.extend(self.chunker.chunk(document))

        return chunks
