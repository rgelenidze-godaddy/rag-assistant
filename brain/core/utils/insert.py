from brain.vectorstore.connection import get_vectorstore


def insert_triples(facts: list[tuple[str, str, str]]) -> str:
    facts_vectorstore = get_vectorstore("facts_collection")

    texts = []
    metadatas = []

    for subject, predicate, obj in facts:
        full_fact = f"{subject} {predicate} {obj}"  # One single string to embed
        texts.append(full_fact)
        metadatas.append({
            "subject": subject,
            "predicate": predicate,
            "object": obj
        })

    facts_vectorstore.add_texts(texts, metadatas)

    return "Learned the facts. Ready to go!"
