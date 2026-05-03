# core/retriever.py

import chromadb
from chromadb.utils import embedding_functions

from config import VECTOR_DB_PATH, COLLECTION_NAME, TOP_K


# Aynı embedding modeli kullanılmalı!
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


def retrieve_context(query: str, role_name: str = "default") -> str:
    """
    Verilen query'e göre en alakalı chunk'ları getirir
    """

    # 1. Chroma client
    client = chromadb.PersistentClient(path=VECTOR_DB_PATH)

    # 2. Collection al
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function
    )

    # 3. Sorgu yap
    results = collection.query(
        query_texts=[query],
        n_results=TOP_K,
        where={"role": role_name}
    )

    # 4. Chunk'ları birleştir
    documents = results.get("documents", [[]])[0]

    context = "\n\n".join(documents)

    return context