from fastapi import APIRouter, Body
from models.schemas import  chatRequest, GenerateResponse
from services.llama_service import  generate_message, build_chat_prompt, inject_system_message

router = APIRouter()

# -------------------------- Example for Swagger --------------------------

CHAT_REQUEST_EXAMPLE = {
    "messages": [
        {
            "role":"user",
            "content":"string"
        }
    ]
}

# -------------------------- Chat Endpoint --------------------------

@router.post("/chat", response_model = GenerateResponse)
def chat (req: chatRequest = Body(example = CHAT_REQUEST_EXAMPLE) ):
    """
    chat endpoint:
    -Validates incoming messages
    -Injects a default system message
    -Builds the prompt
    -Calls llama.cpp for generation
    """
    messages = inject_system_message(req.messages)
    prompt = build_chat_prompt(messages)
    result = generate_message( req, prompt)
    return GenerateResponse(response = result) 