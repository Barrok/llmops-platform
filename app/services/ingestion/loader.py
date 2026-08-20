from pathlib import Path

from pypdf import PdfReader

from app.models.document import Document


class DocumentLoader:
    """Loads supported document files into Document objects."""

    SUPPORTED_FORMATS = {".txt", ".md", ".pdf"}

    def load(self, path: str) -> Document:
        file_path = Path(path)

        if file_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported document format: {file_path.suffix}")

        if file_path.suffix.lower() == ".pdf":
            reader = PdfReader(file_path)
            content = "\n".join(page.extract_text() or "" for page in reader.pages)
        else:
            content = file_path.read_text(encoding="utf-8")

        return Document(
            content=content,
            source=str(file_path),
            metadata={
                "filename": file_path.name,
                "format": file_path.suffix.lower().lstrip("."),
            },
        )
