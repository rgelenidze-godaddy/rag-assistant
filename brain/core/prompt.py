from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnableSequence

from brain.llm import prompts, instance as llm_instance
from brain.core.utils.query import get_doc_rag, get_fact_rag

query_rag = RunnableParallel(
    {
        "prompt": lambda x: x,
        "rag_docs": RunnableLambda(get_doc_rag),
        "rag_facts": RunnableLambda(get_fact_rag)
    }
)
assemble_prompt = RunnableLambda(prompts.PROMPT_MAIN.invoke)
call_llm = llm_instance.get_instance()

prompt_chain = RunnableSequence(
    query_rag,  # retrieve RAG knowledge in parallel from Doc and Fact stores
    assemble_prompt,  # Assemble prompt
    call_llm  # call LLM and return answer
)
