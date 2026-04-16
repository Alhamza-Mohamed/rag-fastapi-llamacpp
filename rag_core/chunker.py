from rag_core.document import Document
import re
from typing import List


def chunk_document(
    documents: List[Document],
    chunk_size: int = 500,
    overlap_sentences: int = 2
) -> List[Document]:
    chunks: List[Document] = []

    for doc in documents: # Loop over documents
        """
        Split a Document into smaller overlapping chunks.

        Parameters:
        - doc: The original Document object.
        - chunk_size: Maximum number of characters per chunk.
        - overlap_sentences: Number of sentences to overlap between chunks.

        Returns:
        - List[Document]: New Document objects representing chunks.
        """

        # Split the document text into sentences.
        # The regex means:
        # (?<=[.!?])  → Split AFTER ., !, or ?
        # \s+         → One or more whitespace characters
        sentences = re.split(r'(?<=[.!?])\s+', doc.text)

        

        i = 0  # Sentence index pointer

        # Loop until we consume all sentences
        while i < len(sentences):

            chunk_sentences = []
            current_length = 0

            start_sentence_index = i  # Remember where this chunk starts

            # Keep adding sentences until we hit chunk_size
            while (
                i < len(sentences)
                and current_length + len(sentences[i]) <= chunk_size
            ):
                sentence = sentences[i]
                chunk_sentences.append(sentence)

                # +1 accounts for space when joining sentences
                current_length += len(sentence) + 1
                i += 1

            # Combine collected sentences into one chunk string
            chunk_text = " ".join(chunk_sentences)

            # Compute character-level metadata
            # We approximate start/end by searching inside original text
            start_char = doc.text.find(chunk_text)
            end_char = start_char + len(chunk_text)

            # Create a NEW Document object for this chunk
            chunk_doc = Document(
                text=chunk_text,
                metadata={
                    "source": doc.metadata["source"],
                    "start": start_char,
                    "end": end_char,
                }
            )

            chunks.append(chunk_doc)

            # Step backward for overlap
            # This allows the next chunk to re-include the last N sentences
            i = max(start_sentence_index + len(chunk_sentences) - overlap_sentences, 0)

    return chunks
