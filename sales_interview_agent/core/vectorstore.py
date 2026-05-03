# core/vectorstore.py

import chromadb
from chromadb.utils import embedding_functions

from core.chunker import chunk_text
from config import VECTOR_DB_PATH, COLLECTION_NAME, CHUNK_SIZE, CHUNK_OVERLAP


# Local embedding modeli
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


def build_vectorstore(text: str, role_name: str = "default"):
    """
    Metni alır, chunk'lara böler ve Chroma'ya kaydeder
    """

    # 1. Chunk oluştur
    chunks = chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)

    # 2. Chroma client başlat
    client = chromadb.PersistentClient(path=VECTOR_DB_PATH)

    # 3. Collection oluştur / varsa al
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function
    )

    # 4. Önce eski veriyi temizle (ilk geliştirme için iyi)
    collection.delete(where={"role": role_name})

    # 5. Chunk'ları ekle
    documents = chunks
    metadatas = [{"role": role_name} for _ in chunks]
    ids = [f"{role_name}_{i}" for i in range(len(chunks))]

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"✅ {len(chunks)} adet chunk Chroma'ya yüklendi.")