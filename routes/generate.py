from fastapi import APIRouter
from models.schemas import GenerateRequest, GenerateResponse
from services.llama_service import build_prompt, generate_text

router = APIRouter()

# -------------------------- API endpoint --------------------------

@router.post("/generate", response_model = GenerateResponse)
def generate (req: GenerateRequest):
    """
    This function is called when:
    POST /generate
    Automatically validates incoming JSON against GenerateRequest
    Automatically returns JSON formatted as GenerateResponse
    """
    
    full_prompt = build_prompt(req.prompt)
    result = generate_text(full_prompt, req)
    return GenerateResponse(response = result)