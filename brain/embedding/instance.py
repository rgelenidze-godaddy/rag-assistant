from brain.embedding.embedder import NomicEmbedder
from brain import settings

# Singleton instance of NomicEmbedder
_embedder_instance: NomicEmbedder | None = None


# Function to initialize the embedder instance
def initialize() -> None:
    global _embedder_instance
    if _embedder_instance is None:
        _embedder_instance = NomicEmbedder(
            settings.EMBEDDER_MODEL,
            settings.EMBEDDER_DIM
        )


# Global function to get/initialize the embedder instance (Singleton)
def get_instance() -> NomicEmbedder:
    initialize()  # Reuse logic from init_embedder
    return _embedder_instance
