from dataclasses import dataclass


@dataclass
class DocumentChunk:
    content: str
    source: str
    metadata: dict[str, str]
