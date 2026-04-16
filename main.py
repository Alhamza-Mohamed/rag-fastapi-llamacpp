# main.py
from fastapi import FastAPI
from rag_setup import build_pipeline
from routes.rag import router as rag_router
from routes.Chat import router as chat_router

app = FastAPI(title="LLM RAG API")

# Build once at startup
pipeline = build_pipeline

# Attach to app state 
app.state.pipeline = pipeline()

app.include_router(rag_router)
