from core.models import Document, TextChunk


class TextChunker:
    """Splits raw text into overlapping fixed-size window chunks."""

    def __init__(self, chunk_size: int = 200, overlap: int = 40) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split_document(self, doc: Document) -> list[TextChunk]:
        """Segments a Document into sequential TextChunks with character overlap."""
        text = doc.content
        chunks: list[TextChunk] = []
        start = 0
        chunk_idx = 0

        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]

            chunk_obj = TextChunk(
                chunk_id=f"{doc.doc_id}_chunk_{chunk_idx}",
                doc_id=doc.doc_id,
                text=chunk_text.strip()
            )
            chunks.append(chunk_obj)

            start += self.chunk_size - self.overlap
            chunk_idx += 1

        return chunks