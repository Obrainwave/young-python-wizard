import numpy as np
import torch

class RetrievalService:
    def __init__(self, document_repo):
        self.document_repo = document_repo

    def retrieve(self, query_embedding, top_k=3):
        """Find top-k most similar document chunks."""
        docs = self.document_repo.get_all()
        if not docs:
            return []
        query_emb = query_embedding.cpu().numpy() if torch.is_tensor(query_embedding) else query_embedding
        similarities = []
        for doc in docs:
            doc_emb = doc.embedding.cpu().numpy() if torch.is_tensor(doc.embedding) else doc.embedding
            sim = np.dot(query_emb, doc_emb) / (np.linalg.norm(query_emb) * np.linalg.norm(doc_emb))
            similarities.append((sim, doc))
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in similarities[:top_k]]