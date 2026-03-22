from rag_core.vector_store import VectorStore
from rag_core.document import Document
from typing import List,Dict

class Retriever:
    """
    High-level retrieval logic on top of VectorStore
    Handles top-k section, duplicate removal, and optional per-file quotas.
    """
    
    def __init__(self, store: VectorStore):
        """
        Args: store an instance of VectorStore
        """
        self.store = store

    def retrieve(self, query_embedding: List[float], top_k: int = 5, filter_source: str | None = None, per_file_quota: Dict[str, int] | None = None) -> List[Document]: 
        # filter_source: str | None = None filter source can be str or none and the default = none 
         """
         Retrieve top-k relevant Document chunks, with optional filtering and duplicate removal.
        
         Args:
            query_embedding: Embedding vector of the query
            top_k: Number of chunks to return
            filter_source: Optional, only retrieve chunks from a specific source file name
            per_file_quota: optional dict {source_filename: number_of_chunks} to guarantee per-file counts
         
         Returns:
            List[Document]: final retrieved chunks
         """
         # Step 1: get similarity-ranked results
         # Fetch extra candidates to allow filtering/deduplicate/per-file quota
         buffer_multiplier = 3 # Ensures candidates survive filtering, deduplication, and per-file quotas
         fetch_k = top_k * buffer_multiplier if not per_file_quota else max(per_file_quota.values()) * buffer_multiplier
         candidates = self.store.search(query_embedding, top_k = fetch_k)
         



         # Step  2: optional source filtering
         if filter_source is not None:
             candidates = [(score, doc) for score, doc in candidates if doc.metadata.get("source") == filter_source]
             """
             doc.metadata = {
                 "source": "fileA.txt",
                 "page": 3,
                 "chunk_id": 12
             }
             instead of doc.metadata["source"] we use doc.metadata.get("source")
             bec: metadata["source"] → throws KeyError if "source" doesn't exist, metadata.get("source") → returns None if it doesn't exist

             """
        
        # Step 3: remove duplicates caused by overlapping chunks 
         seen_texts = set()
         final_docs : List[Document] = []

        # step 4: per-file quotas handling
         if per_file_quota:
             counters = {file: 0 for file in per_file_quota} 
             # dictionary comprehension. It uses the keys (file) from per_file_quota as a template and give it initial value of 0 {file (str) , 0(int)}

             for score, doc in candidates:
                 text = doc.text
                 source = doc.metadata.get("source")

                 # Skip duplicates
                 if text in seen_texts:
                     continue
                 # Skip if source not in quotas
                 if source not in counters:
                     continue
                 
                 # Accept the doc only if we haven't hit the quota for this specific file
                 if counters[source] < per_file_quota[source]:
                    final_docs.append(doc)
                    seen_texts.add(text)
                    counters[source] +=1
                
                 else:
                 # We already have enough of this file, so skip this chunk
                    continue

                 # Stop early if all quotas satisfied
                 if all(counters[src] >= per_file_quota[src] for src in counters):
                     break
                     """
                     src represents the key (the filename string)
                     counters[src] the current number of chunks that have actually collected for that file
                     per_file_quota[src] the target number wanted for that file
                     all(...) function returns True only if every single item in the loop meets the condition
                     """
             
         else:
             # No per-file quotas, simple top_k selection with deduplication
             for score, doc in candidates:
                 text = doc.text
                 if text in seen_texts:
                     continue
                 final_docs.append(doc) # final_docs is list, list -> append
                 seen_texts.add(text) # seen_text is set, set-> add 
                 if len(final_docs) >= top_k:
                    break
         return final_docs
            