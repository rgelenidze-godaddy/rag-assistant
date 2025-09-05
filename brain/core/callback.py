from brain.core.prompt import prompt_chain
from brain.core.teach import teach_chain
from brain.core.utils.update_rag import update_documents_store


def brain_callback_sync(text: str, action="PROMPT") -> str:
     if action == "PROMPT":
          return prompt_chain.invoke(text).content
     elif action == "TEACH":
          return teach_chain.invoke(text)
     elif action == "UPDATE_RAG":
          updated_files = update_documents_store()

          return f"""
          Updated documents store with {len(updated_files)} documents.\n
          {',\n'.join(updated_files)}
          """
     else:
          raise ValueError(f"Unknown action: {action}")


