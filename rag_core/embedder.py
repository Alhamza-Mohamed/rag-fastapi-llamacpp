import numpy as np
import hashlib 
from typing import List

class SimpleEmbedder:
    """
    Deterministic development embedder using token hashing
    
    word-level tokenization
    Hashing trick for fixed-size vector
    Frequency-based encoding
    No normalization (handled by VectorStore)  
    """
    def __init__(self, dim : int =384):
        self.dim = dim

    def _hash_token(self, token: str) -> int:
        """
        Stable hash function for tokens.
        Uses MD5 to ensure deterministic behavior across runs.
        """
        
        return int(hashlib.md5(token.encode()).hexdigest(), 16)
        """
        Takes token and runs it through the MD5 hashing algorithm
        MD5 algorithm cant read regular python text strings(Unicode) so it requires a raw stream of bytes
        .encode() translate the text token into byte object to be read by MD5 algorithm.
        The result MD5 always turns the same token into the same long hexadecimal string.
        the hex string made of hexadecimal characters (numbers 0-9 and letters a-f). ex "1f3870be274f6c49b3e31a0c6728957f".
        By converting the hex string into an integer using int(..., 16) - so we can apply math on it - the output is a massive unique int that represent the specific piece of text
        """
        
    def embed_documents(self, texts: List[str]) -> np.ndarray:
        """
        Convert a list of texts into embedding vectors.

        Args: 
            texts: List of input
        Return:
            np.ndarray of shape (N, dim)

        """
        N = len(texts) # N is the number of strings (documents/sentences) in the list, not the total number of words.
        embeddings = np.zeros ((N, self.dim), dtype= np.float32 ) # 2D NumPy array of shape (Number_of_Documents * dim or 384).

        for i, text in enumerate(texts): # iterating through every text in the texts (documents) 
            # i is the number of how many times word appear 

            # Normalize text (all uppercase to lowercase)
            text = text.lower()

            # Simple tokenization 
            tokens = text.split()

            for token in tokens: # iterating through every word in a single document
                # Hash token -> index
                index = self._hash_token(token) % self.dim

                # Increment frequency (detect the number of appearance of each word)
                embeddings[i, index] += 1.0

        """
        Each row 'i' is a vector representing one document.
        Each column 'index' is a 'bucket' representing a word (or group of words via hashing).
        The value at embeddings[i, index] is the 'Term Frequency'—how many times 
        words in Document i mapped to that specific dimension.
        """
        return embeddings

    def embed_query (self, text: str) -> np.ndarray:
        """
        Convert a single query string into an embedding vector.
        
        Returns:
            np.ndarray of shape (dim,)
        """
        return self.embed_documents([text])[0]