import os
import hashlib

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

from brain import settings
from brain.vectorstore import connection as vectorstore_connection


def file_hash(path: str) -> str:
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def hash_exists(doc_hash: str) -> bool:
    client = vectorstore_connection.get_connection()

    response = client.scroll(
        collection_name="documents_collection",
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="metadata.hash",
                    match=MatchValue(value=doc_hash)
                )
            ]
        ),
        limit=1,
        with_payload=True
    )

    return len(response[0]) > 0


def update_documents_store():
    docs_vectorstore = vectorstore_connection.get_vectorstore("documents_collection")
    inserted_files = []

    for filename in os.listdir(settings.DOCS_DIR):
        # Accept only PDF files
        if not filename.endswith(".pdf"):
            continue

        path = os.path.join(settings.DOCS_DIR, filename)

        if not os.path.isfile(path):
            continue

        doc_hash = file_hash(path)

        if hash_exists(doc_hash):
            print(f"Skipped (already exists): {filename}")
            continue
        else:
            print(f"Processing: {filename}")

        # Load the document and split into chunks
        docs = PyMuPDFLoader(path).load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=750,
            chunk_overlap=75,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        split_docs = splitter.split_documents(docs)

        # Embed and insert into vectorstore
        texts = [doc.page_content for doc in split_docs]

        # Create metadata for each chunk (filename and hash)
        metadatas = [{"source": filename, "hash": doc_hash} for _ in split_docs]

        # Add chunks to the vectorstore
        docs_vectorstore.add_texts(
            texts=texts,
            metadatas=metadatas
        )

        inserted_files.append(filename)
        print(f"Uploaded: {filename}")

    return inserted_files


if __name__ == "__main__":
    update_documents_store()
