import os, pickle
from pathlib import Path
import faiss, numpy as np
from .llm_clients.embeddings_ollama import OllamaEmbeddingClient

class FaissStore:
    def __init__(self):
        self.index = None
        self.records = []

    def build(self, embeddings: np.ndarray, records):
        embeddings = (embeddings / (np.linalg.norm(embeddings, axis=1, keepdims=True)+1e-12)).astype(np.float32)
        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings)
        self.records = records

    def search(self, qvec: np.ndarray, k=6):
        qvec = (qvec / (np.linalg.norm(qvec, axis=1, keepdims=True)+1e-12)).astype(np.float32)
        D, I = self.index.search(qvec, k)
        return [(float(D[0][i]), self.records[I[0][i]]) for i in range(len(I[0])) if I[0][i] != -1]

def embed_texts(texts, base_url, model):
    client = OllamaEmbeddingClient(base_url, model)
    return client.embed(texts)