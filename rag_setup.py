from rag_core.loader import  load_text_files
from rag_core.chunker import chunk_document
from rag_core.embedder import TransformerEmbedder
from rag_core.vector_store import VectorStore
from rag_core.retriever import Retriever
from rag_core.prompt import PromptBuilder
from rag_core.pipeline import Pipeline
from rag_core.llm import LlamaLLM 


def build_pipeline() -> Pipeline:

    # 1. Load documents
    documents = load_text_files("data")

    
    # 2.Chunk
    chunks = chunk_document(documents,chunk_size=500, overlap_sentences=2) 
    
    
    # 3. Embed
    embedder = TransformerEmbedder()
    texts = [doc.text for doc in chunks] # separate the text from the whole documents
    vectors = embedder.embed_documents(texts) # embedder deals with text only not documents

    # 4. Store
    vector_store = VectorStore()
    for vec, doc in zip(vectors, chunks):
        vector_store.add(vec,doc) # add vectors one by one 

    # 5. Retriever
    retriever = Retriever(vector_store) 
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

    

    return pipeline