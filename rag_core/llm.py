from typing import List, Dict
from services.llama_service import build_chat_prompt,generate_message
from models.schemas import ChatMessage, chatRequest

class LlamaLLM:
    def __init__(self, temperature = 0.7, top_p = 0.9, n_predict = 256 ):
        self.temperature= temperature
        self.top_p = top_p
        self.n_predict = n_predict

    #def generate(self, message: List[Dict[str,str]]) -> str:


        