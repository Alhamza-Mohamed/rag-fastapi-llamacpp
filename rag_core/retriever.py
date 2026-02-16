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

    def retrieve(self, query_embedding: List[float], top_k: int = 5, filter_source: str = None) -> List[Document]:
         """
         Retrieve top-k relevant Document chunks, with optional filtering and duplicate removal.

         Args:
            query_embedding: Embedding vector of the query
            top_k: Number of chunks to return
            filter_source: Optional, only retrieve chunks from a specific source file name
         """
         # Step 1: retrieve all candidate chunks from the vector store
         candidates = self.store.retrieve(query_embedding, top_k = len(self.store.store))

         # Step  2: optional source filtering
         if filter_source:
             candidates = [doc for doc in candidates if doc.metadata.get("source") == filter_source]
        
        # Step 3: remove duplicates caused by overlapping chunks 
         seen_texts = set()
         unique_docs = []
         for doc in candidates:
             if doc.text not in seen_texts:
                 unique_docs.append(doc)
                 seen_texts.add(doc.text)
             if len(unique_docs) >= top_k:
                 break
         return unique_docs
            