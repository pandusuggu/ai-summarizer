from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingEngine:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def get_embeddings(self, texts: list) -> np.ndarray:
        """Generates embeddings for a list of strings."""
        if not texts:
            return np.array([])
        return self.model.encode(texts)

    def compute_similarity(self, emb1, emb2):
        """Computes cosine similarity between two embeddings."""
        return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

if __name__ == "__main__":
    print("Embedding engine initialized.")
