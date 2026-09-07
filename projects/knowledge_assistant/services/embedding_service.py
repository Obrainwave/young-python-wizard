from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts):
        """Convert a list of texts to embeddings."""
        return self.model.encode(texts, convert_to_tensor=True)

    def embed_single(self, text):
        """Convert a single text to an embedding."""
        return self.model.encode(text, convert_to_tensor=True)