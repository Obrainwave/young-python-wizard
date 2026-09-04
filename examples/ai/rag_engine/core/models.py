from dataclasses import dataclass, field
from typing import Any


@dataclass
class Document:
    """Represents a raw input document."""
    doc_id: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TextChunk:
    """Represents a segmented text block extracted from a Document."""
    chunk_id: str
    doc_id: str
    text: str
    embedding: list[float] = field(default_factory=list)


@dataclass
class SearchResult:
    """Encapsulates a retrieved chunk alongside its similarity score."""
    chunk: TextChunk
    score: float