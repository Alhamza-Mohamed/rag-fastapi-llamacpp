import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer

class TransformerEmbedder:
    """
    Production-grade embedder using SentenceTransformer

    - Semantic embeddings (not just token counts)
    - Handles context and meaning
    - Return dense vectors
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts:List[str]) -> np.ndarray:
        """
        Convert list of texts into embeddings

        return:
            np.ndarray of shape (N,dim)
        """
        embeddings = self.model.encode(
            texts,
            convert_to_numpy = True,
            normalize_embeddings = False # already normalized in VectorStore
        )
        return embeddings
    
    def embed_query(self, text:str) ->np.ndarray:
        """
        Convert single query into embedding

        Returns:
            np.ndarray of shape (dim,)
        """
        return self.embed_documents([text])[0] # Reuse batch embedding (expects List [str]) -> returns (1,dim), 
                                               # then extract the single vector ->(dim,)
                                               # i.e. wrap text in list for batch API, then unwrap the single result