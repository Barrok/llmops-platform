from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.models.chunk import DocumentChunk
from app.models.document import Document


class DocumentChunker:
    """Splits documents into overlapping chunks."""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def chunk(self, document: Document) -> list[DocumentChunk]:
        chunks = self.splitter.split_text(document.content)

        return [
            DocumentChunk(
                content=content,
                source=document.source,
                metadata={
                    **document.metadata,
                    "chunk_index": str(index),
                },
            )
            for index, content in enumerate(chunks)
        ]
