from brain import settings
from brain.vectorstore.connection import get_vectorstore


def _get_rag_matches(collection_name, prompt):
    """Generic function to get RAG matches from any collection."""
    vectorstore = get_vectorstore(collection_name)
    matches = vectorstore.similarity_search_with_score(prompt)

    # Get threshold passing matches
    return [doc.page_content for doc, score in matches if score >= settings.SIMILARITY_THRESHOLD]


def get_doc_rag(prompt):
    return _get_rag_matches("documents_collection", prompt)


def get_fact_rag(prompt):
    return _get_rag_matches("facts_collection", prompt)