from typing import List, Dict
from rag_core.document import Document

class PromptBuilder:
    def __init__(self, default_instruction: str | None = None):
        self.default_instruction = default_instruction or (
    "You are a helpful AI assistant.\n"
    "Use ONLY the provided context to answer the question.\n"
    "If the answer is not explicitly in the context, say: 'I don't know.'\n"
    "Do NOT use prior knowledge. \n"
    "Cite the chunk numbers when relevant. "
    )
    
    def build (self, query: str, documents: List[Document], instruction: str | None = None
    ) -> List  [Dict[str,  str]]:  
        # Resolve instruction  (default vs override)
        instruction = instruction or self.default_instruction

        system_msg = self._format_instruction(instruction)
        context = self._format_context(documents)
        user_msg =  self._format_user_message(query, context)

        return[system_msg,user_msg]
    
    def _format_instruction(self, instruction: str) -> Dict[str, str]:
        return {
            "role":"system",
            "content":instruction
        }
    
    def _format_context(self, documents: List[Document]) -> str:
        chunks = []

        for i,doc in enumerate(documents, start=1):
            source = doc.metadata.get("source", "unknown")
            start = doc.metadata.get("start", "N/A")
            end = doc.metadata.get("end", "N/A")

            chunk_text = (
                f"Chunk {i}:\n"
                f"Source: {source}\n"
                f"Position: {start} - {end}\n"
                f"Content:\n{doc.text}"
            )

            chunks.append(chunk_text)

        return  "\n\n".join(chunks)

    def _format_user_message(self, query: str, context: str) -> Dict[str,str]:
        content =(
            "You are given the following context:\n\n"
            "===== CONTEXT START =====\n"
            f"{context}\n\n"
            "===== CONTEXT END =====\n\n"
            "Answer the question using ONLY the context above."
            "If the answer is not in the context, say: 'I dont know'\n\n"
            f"Question: {query}\n\n"
            
        )

        return{
            "role": "user",
            "content": content
        }