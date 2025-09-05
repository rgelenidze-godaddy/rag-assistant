from langchain_core.output_parsers import JsonOutputParser
from langchain.chains import LLMChain

from brain.llm import instance as llm_instance
from brain.llm import prompts


def extract_fact_triples(prompt: str) -> list[tuple[str, str, str]]:
    """
    Extract fact triples from the given prompt using the LLM.
    """
    # Get your singleton LLM
    llm = llm_instance.get_instance()

    # Build chain
    extract_triples_chain = LLMChain(
        llm=llm,
        prompt=prompts.PROMPT_EXTRACT_FACTS,
        output_parser=JsonOutputParser()
    )

    # Call chain with your input
    triples: list[list[str, str, str]] = extract_triples_chain.invoke({"prompt": prompt})["text"]

    # Normalize and convert each triple to tuple
    canonical_triples = [
        tuple(part.strip().lower() for part in triple)
        for triple in triples
    ]

    return canonical_triples