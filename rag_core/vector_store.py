from typing import List, Tuple
import numpy as np
from rag_core.document import Document

class VectorStore: 
    """
    simple in-memory vector store for RAG.
    Stores (embedding, Document) tuples and supports top-l cosine similarity return
    """

    def __init__(self):
        # Store is a list of tuples: (normalized_embedding, Document)
        self.store: List[Tuple[np.ndarray, Document]] = []

    def add(self, embedding: List[float], doc: Document) -> None:
        """
        Add a new chunk embedding + document to the store
        
        Args: 
            embedding: List of floats representing the chunk embedding
            doc: Document object containing text + metadata
        """
        # convert to numpy array for vector math
        vec = np.array(embedding, dtype=np.float32)

        # Normalize vector to unit length for cosine similarity
        norm = np.linalg.norm(vec)
        if norm != 0:
            # Edge case: zero vector
             vec = vec/norm
        
        # Append tuple to the store
        self.store.append((vec,doc))

    def search( self, query_embedding: List[float], top_k: int = 5)-> List[Tuple[float,Document]]:
        """
        perform cosine similarity search
        Returns:
            List of (similarity_score, Document) stored descending
        """ 

        if not self.store:
            return []
        #if the list is empty. If you haven't added any documents yet, self.store is []. In Python, an empty list evaluates to False. So this line prevents the code from trying to search through nothing 
        
        query_vec = np.array(query_embedding, dtype=np.float32)
        norm = np.linalg.norm(query_vec)
        if norm !=0:
            query_vec = query_vec/norm
            
        results: List[Tuple[float, Document]] = []
        
        for vec, doc in self.store:
            score = float(np.dot(query_vec,vec))
            results.append((score, doc))

        # sort descending by similarity
        results.sort(key = lambda x:x[0], reverse = True)
        """
          results: This is a list of tuples that looks like this: [(0.92, doc1), (0.45, doc2), (0.88, doc3)].
            lambda x: x[0]: This is a "throwaway" function. It tells Python: "For every item 'x' in the list (which is a tuple), look at index 0 (the score)."
            key: This tells the sort function to use the score to decide the order, rather than trying to compare the Document objects (which Python wouldn't know how to do).
            reverse = True: By default, Python sorts from smallest to largest. In RAG, we want the highest similarity score first, so we reverse it.
              """
        return results [:top_k]