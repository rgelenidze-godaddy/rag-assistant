from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from qdrant_client.http.models import Distance, VectorParams

from brain.embedding import instance as embedding_instance
from brain import settings

_client_instance: QdrantClient | None = None


def initialize() -> None:
    global _client_instance
    if _client_instance is None:
        _client_instance = QdrantClient(url=settings.QDRANT_URL)


def get_connection() -> QdrantClient:
    initialize()
    return _client_instance


def get_vectorstore(collection_name: str) -> QdrantVectorStore:
    return QdrantVectorStore(
        client=get_connection(),
        embedding=embedding_instance.get_instance(),
        collection_name=collection_name
    )


def declare_collections() -> None:
    """
    Declare collections in Qdrant.
    """
    client = get_connection()

    existing_collections = {collection.name for collection in client.get_collections().collections}
    absent_collections = set(settings.COLLECTIONS) - existing_collections

    # Check if collection exists, if not create it
    for collection_name in absent_collections:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=settings.EMBEDDER_DIM,
                distance=Distance.COSINE
            )
        )
