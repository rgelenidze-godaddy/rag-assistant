import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, 'brain', 'docs')

# Vector store (Qdrant)
QDRANT_URL = os.getenv("QDRANT_URL")
SIMILARITY_THRESHOLD = 0.65

COLLECTIONS = {"documents_collection", "facts_collection"}

# LLM module (see https://aistudio.google.com/)
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
LLM_MODEL = "gemini-1.5-flash"
LLM_TEMPERATURE = 0
DISABLE_STREAMING = True

# Embedder module (see https://huggingface.co/nomic-ai/nomic-embed-text-v1.5)
EMBEDDER_MODEL = "nomic-ai/nomic-embed-text-v1.5"
EMBEDDER_DIM = 768