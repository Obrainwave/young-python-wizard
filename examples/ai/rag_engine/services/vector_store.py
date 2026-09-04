from core.models import TextChunk, SearchResult
from core.math_utils import cosine_similarity


class VectorStore:
    """In-memory dense vector index executing exact Cosine Nearest Neighbor search."""

    def __init__(self) -> None:
        self.index: list[TextChunk] = []

    def add_chunks(self, chunks: list[TextChunk]) -> None:
        """Appends embedded chunks into the vector repository."""
        self.index.extend(chunks)

    def search(self, query_vector: list[float], top_k: int = 2) -> list[SearchResult]:
        """Performs vector similarity search over the indexed corpus."""
        results: list[SearchResult] = []

        for chunk in self.index:
            score = cosine_similarity(query_vector, chunk.embedding)
            results.append(SearchResult(chunk=chunk, score=score))

        # Sort descending by similarity score
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]