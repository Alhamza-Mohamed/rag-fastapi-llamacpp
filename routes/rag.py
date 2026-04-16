from fastapi import APIRouter, Request
from pydantic import  BaseModel

"""
API router: mini "router" object that groups related endpoints, it is like a chapter in a book.
the main app can include multiple routers

Request: gives access to the raw HTTP request object

BaseModel: a Pydantic class that allow define the shape of incoming data and automatically validates it
"""

router = APIRouter() 

class RAGRequest(BaseModel):
    query:str # define what the request must look like
"""
Means whoever call this endpoint must send a JSON body with a field called query
If they send the wrong type or forget the field, FastAPI rejects the request automatically with a helpful error — no manual validation needed.
"""

@router.post("/rag") # This decorator registers the function below it as a POST handler at the path /rag. When someone sends a POST request to /rag, this function runs.
def rag_endpoint(req: RAGRequest, request: Request):
    pipeline = request.app.state.pipeline
    result = pipeline.run(req.query)
    return result

"""
- 'req: RAGRequest': FastAPI reads the JSON body and *automatically* parses it into 'RAGRequest' object so 'req.query' give you the query string the user sent
- 'request: Request' -: the raw request object, here it is used to access 'request.app.state.pipeline', which is a RAG pipeline object that was stored on the app when it started up (a common pattern for sharing resources like DB connections or ML pipelines across endpoints)
- 'pipeline.run(req.query)': runs the RAG pipeline with the user's query
- 'return result': FastAPI automatically converts the returned value to a JSON response
---

**The big picture flow**

user sends: POST /rag {"query": "what is X?"}
                  ↓
FastAPI validates body -> creates RAGRequest(query = "what is X?")
                  ↓
Handler grabs the pipeline from app.state
                  ↓
pipeline.run("what is X?") -> result
                  ↓
FastAPI returns result as JSON response
                  
"""
