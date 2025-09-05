from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()

PROMPT_EXTRACT_FACTS = PromptTemplate(
    template="""
You are a strict AI assistant that extracts only factual triples from user input.

Extract all facts from the prompt and return them as raw JSON in the following format:

[["type:subject", "predicate", "type:object"], ...]
[["University:Stanford", "located in", "Country:USA"], ...]

If you encounter same entities or predicates (university, same person, etc.) try to make the name canonical so they are mentioned the same way.


Do NOT include:
- Markdown (```json)
- Explanations
- Comments

PROMPT: {prompt}
EXTRACTED FACTS:
""",
    input_variables=["prompt"],
    output_parser=parser
)


PROMPT_MAIN = PromptTemplate(
    template="""
You are an intelligent AI assistant, assisted with RAG knowledge for contextual understanding.

QUESTION: {prompt}

[DOCUMENT CONTEXT]
{rag_docs}

[FACT CONTEXT]
{rag_facts}j

Answer the QUESTION in a natural way, as if you are a human.
In your answer, please don't mention the documents or context are used.
Act like a normal LLM answering a question. Its not necessary to use all the context.
Maybe its not even necessary to use any of the context, answer normally as LLM would.
If question can not be answered because of lack of context, it's ok to say "I don't know".
""",
    input_variables=["prompt", "rag_docs", "rag_facts"]
)
