from typing import List, Dict
from services.llama_service import build_chat_prompt,generate_message
from models.schemas import ChatMessage, chatRequest

class LlamaLLM:
    def __init__(self, temperature = 0.7, top_p = 0.9, n_predict = 256 ):
        self.temperature= temperature
        self.top_p = top_p
        self.n_predict = n_predict

    def generate(self, messages: List[Dict[str,str]]) -> str:
        """
        message: List[{"role: "...", "content": "..."}]
        """

        # Convert dict into ChatMessage (the existing schema)
        chat_messages = [
            ChatMessage(role = m ["role"], content = m["content"])
            for m in messages
        ]
        
        # Build prompt string for llama.cpp
        prompt = build_chat_prompt (chat_messages)

        # Create request object (reuse the schema)
        req = chatRequest(
            messages=chat_messages,
            n_predict = self.n_predict,
            temperature = self.temperature,
            top_p = self.top_p,
        )

        # Call the existing llama.cpp service
        return generate_message  (req,prompt )