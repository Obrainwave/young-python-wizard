import math


class MockEmbeddingGenerator:
    """
    Generates deterministic continuous vectors for demonstration.
    In production environments, replace with OpenAI, Sentence-Transformers, or Ollama.
    """

    def __init__(self, dimension: int = 16) -> None:
        self.dimension = dimension

    def embed_text(self, text: str) -> list[float]:
        """Generates a normalized float vector based on character hash distributions."""
        vector = [0.0] * self.dimension
        for i, char in enumerate(text):
            idx = (ord(char) + i) % self.dimension
            vector[idx] += math.sin(ord(char)) + 1.0

        # Normalize vector to unit length
        norm = math.sqrt(sum(x * x for x in vector))
        if norm > 0:
            vector = [x / norm for x in vector]

        return vector