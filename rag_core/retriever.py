from rag_core.vector_store import VectorStore
from rag_core.document import Document
from typing import List

class Retriever:
    """
    High-level retrieval logic on top of VectorStore
    Handles top-k section, duplicate removal, and metadat-aware filtering
    """

    def __init__(self, store: VectorStore):
        """
        Args: store an instance of VectorStore
        """
        self.store = store

    def retrieve(self, query_embedding: List[float], top_k: int = 5, filter_source: str | None = None) -> List[Document]: 
        # filter_source: str | None = None fileter source can be str or none and the defult = none 
         """
         Retrieve top-k relevant Document chunks, with optional filtering and duplicate removal.

         Args:
            query_embedding: Embedding vector of the query
            top_k: Number of chunks to return
            filter_source: Optional, only retrieve chunks from a specific source file name
         """
         # Step 1: get similarity-ranked results
         candidates = self.store.search(query_embedding, top_k = top_k * 3)

         # Step  2: optional source filtering
         if filter_source:
             candidates = [(score, doc) for score, doc in candidates if doc.metadata.get("source") == filter_source]
        
        # Step 3: remove duplicates caused by overlapping chunks 
         seen_texts = set()
         final_docs : List[Document] = []

         for score, doc in candidates:
             if doc.text not in seen_texts:
                 final_docs.append(doc)
                 seen_texts.add(doc.text)
             if len(final_docs) >= top_k:
                 break
         return final_docs
            