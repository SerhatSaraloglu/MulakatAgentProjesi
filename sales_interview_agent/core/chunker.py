# core/chunker.py

from typing import List


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        # overlap kadar geri gelerek devam et
        start = end - overlap

        if start < 0:
            start = 0

    return chunks