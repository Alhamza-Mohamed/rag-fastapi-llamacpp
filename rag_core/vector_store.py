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

    def add(self, embedding: List[float], doc: Document):
        """
        Add a new chunk embedding + document to the store
        
        Args: 
            embedding: List of floats representing the chunk embedding
            doc: Documnet object containing text + metadata
        """
        # convert to numpy array for vector math
        vec = np.array(embedding, dtype=np.float32)

        # Normalize vector to unit length for cosine similarity
        norm = np.linalg.norm(vec)
        if norm == 0:
            # Edge case: zero vector
            vec = vec
        else:
            vec = vec/norm

        # Append tuple to the store