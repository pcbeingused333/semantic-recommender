from sentence_transformers import SentenceTransformer
import torch
import os

# Load model once when the module is imported
model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
device = "cuda" if torch.cuda.is_available() else "cpu"

embedding_model = SentenceTransformer(model_name, device=device)

def get_embedding(text: str) -> list[float]:
    """Generate embedding for a single text"""
    return embedding_model.encode(text, convert_to_tensor=False).tolist()


def get_embeddings(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for multiple texts (batch)"""
    return embedding_model.encode(texts, convert_to_tensor=False).tolist()