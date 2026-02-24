from dataclasses import dataclass
from typing import Dict

@dataclass
class Document:
    #Represents a single unit of retrievable text
    def __init__(self, text: str, metadata: Dict | None = None):
    

        self.text = text # The actual text content that can be used by the LLM
        self.metadata =  metadata or {} # Dictionary containing tracing/debug info like source filename, start and character positions in the original document.
                                        # metadata can not = None