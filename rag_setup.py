from rag_core.loader import  load_text_files
from rag_core.chunker import chunk_document
from rag_core.embedder import SimpleEmbedder
from rag_core.vector_store import VectorStore
from rag_core.retriever import Retriever
from rag_core.prompt import PromptBuilder
from rag_core.pipeline import Pipeline
from rag_core.llm import LlamaLLM 


def build_pipeline() -> Pipeline:
    # 1. Load documents
    documents = load_text_files("llama.cpp/data")

    # 2.Chunk
    chunks = chunk_document(documents,chunk_size=500, overlap_sentences=50)
    
    # 3. Embed
    embedder = SimpleEmbedder()
    vectors = embedder.embed_documents(chunks)

    # 4. Store
    vector_store = VectorStore()
    vector_store.add(vectors,chunks)

    # 5. Retriever
    retriever = Retriever(vector_store) # it was Retriever(vector_store, top_k = 5) and it caused an error

    # 6. Prompt builder
    prompt_builder = PromptBuilder()

    # 7. LLm
    llm = LlamaLLM() 

    # 8. Pipeline
    pipeline = Pipeline(
        embedder= embedder,
        retriever=retriever,
        prompt_builder=prompt_builder,
        llm = llm 
    )

    print("BUILDING PIPELINE...")

    return pipeline