from abc import ABC

from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings
import torch.nn.functional as F
import threading

class NomicEmbedder(Embeddings, ABC):
    def __init__(self, model_name, dim):
        self.model = SentenceTransformer(model_name, trust_remote_code=True)
        self.dim = dim
        self._lock = threading.Lock()

    def encode(self, texts, prefix):
        texts = [f"{prefix}: {t}" for t in texts]

        # Use a thread lock on model encode, as it is not thread-safe, causing wrong results in parallelism
        with self._lock:
            vec = self.model.encode(texts, convert_to_tensor=True)

        # Safety check
        if self.dim > vec.shape[1]:
            raise ValueError(f"self.dim ({self.dim}) exceeds model output dim ({vec.shape[1]})")

        vecs = F.layer_norm(vec, normalized_shape=(vec.shape[1],))
        vecs = vecs[:, :self.dim]
        vecs = F.normalize(vecs, p=2, dim=1)

        return vecs.tolist()

    # Task-specific methods for encoding (nomic-ai enforces the prefix for better performance)
    def embed_documents(self, texts):
        return self.encode(texts, prefix="search_document")

    def embed_query(self, text):
        return self.encode([text], prefix="search_query")[0]