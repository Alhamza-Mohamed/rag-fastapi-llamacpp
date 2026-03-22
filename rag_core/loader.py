from pathlib import Path
from typing import List
from rag_core.document import Document

def load_text_files(directory: str) -> List[Document]:
    """
    Load all.txt files from a directory and return them as Document objects.
    Each file becomes exactly one Document
    """
    documents : List[Document] = []

    for file_path in Path(directory).glob("*.txt"): # glob("*.txt") means find every thing that ends in .txt within that folder
        text = file_path.read_text(encoding="utf-8") # read_text: It opens the file, reads all the words inside, and saves them to the variable text

        doc = Document(
            text=text,
            metadata={
                "source": file_path.name
            }
        )
        documents.append(doc)

    return documents