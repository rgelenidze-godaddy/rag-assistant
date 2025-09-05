from brain.core.utils.extract import extract_fact_triples
from brain.core.utils.insert import insert_triples

from langchain.schema.runnable import RunnableSequence, RunnableLambda

teach_chain = RunnableSequence(
    RunnableLambda(extract_fact_triples),  # Extract fact triples from user input
    RunnableLambda(insert_triples)  # Insert normalized triples into facts vectorstore collection
)
