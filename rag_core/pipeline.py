from typing import List, Dict

class Pipeline:
    def __init__(self, embedder, retriever, prompt_builder ):
        self.embedder  = embedder
        self.retriever = retriever
        self.prompt_builder = prompt_builder 
         
    def run(self, query: str, top_k: int = 5) -> List [Dict[str, str]]:
        # 1- Embed query
        query_vector = self.embedder.embed(query)

        # 2- Retrieve relevant documents
        documents = self.retriever.retrieve(query_vector,top_k = top_k)

        # 3- Build prompt
        prompt = self.prompt_builder.build(query, documents)

        # Return prompt (debug stage)
        return prompt