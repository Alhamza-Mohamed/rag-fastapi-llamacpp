from typing import List, Dict
from rag_core.document import Document

class Pipeline:
    def __init__(self, embedder, retriever, prompt_builder, llm ):
        self.embedder  = embedder
        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.llm = llm  
         
    def run(self, query: str, top_k: int = None) -> Dict:
        """
        Full RAG flow:
        1. Embed query
        2. Retrieve relevant documents
        3. Build prompt
        4, Generate answer via LLM
        5. return structured response 
        """
        # 1- Embed query
        query_vector = self.embedder.embed_query(query)

        # 2- Retrieve relevant documents
        documents: List[Document] = self.retriever.retrieve(query_vector,top_k = top_k)
        if not documents: # empty document
            return "I dont know"

        # 3- Build prompt
        messages: List[Dict[str, str]] = self.prompt_builder.build(query, documents)

        # 4. Generate answer from LLM
        answer = self.llm.generate(messages)

        # 5. Serialize sources 
        sources = [
            {
                "text": doc.text,
                "metadata": doc.metadata
            }
            for doc in documents
        ]
        
        # Return structured result
        return {
            "answer": answer,
            "sources": sources
            }