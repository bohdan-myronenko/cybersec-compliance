import numpy as np, requests, os

class OllamaEmbeddingClient:
    def __init__(self, base_url: str, model: str, timeout: int = 120):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def embed(self, texts):
        embs = []
        for t in texts:
            r = requests.post(f"{self.base_url}/api/embeddings",
                              json={"model": self.model, "prompt": t},
                              timeout=self.timeout)
            r.raise_for_status()
            embs.append(np.array(r.json()["embedding"], dtype=np.float32))
        return np.vstack(embs)