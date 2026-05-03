from core.loader import load_knowledge
from core.chunker import chunk_text

text = load_knowledge("data/knowledge/sales_consultant.txt")

chunks = chunk_text(text)

print(f"Toplam chunk sayısı: {len(chunks)}\n")

for i, chunk in enumerate(chunks[:3]):
    print(f"Chunk {i+1}:\n{chunk}\n")