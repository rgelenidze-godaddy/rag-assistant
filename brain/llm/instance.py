from langchain_google_genai import ChatGoogleGenerativeAI

from brain import settings

_llm_instance: ChatGoogleGenerativeAI | None = None


def initialize() -> None:
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            disable_streaming=settings.DISABLE_STREAMING
        )


def get_instance():
    initialize()  # verify that the LLM is initialized
    return _llm_instance
