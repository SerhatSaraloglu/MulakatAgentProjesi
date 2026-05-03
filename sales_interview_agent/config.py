# config.py

from dotenv import load_dotenv
import os

# .env dosyasını yükle
load_dotenv()

# ==============================
# 🔗 LM STUDIO AYARLARI
# ==============================
LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
LM_STUDIO_API_KEY = os.getenv("LM_STUDIO_API_KEY", "lm-studio")

# 👇 MODELİNİ BURADA TANIMLIYORUZ
LLM_MODEL = os.getenv("LLM_MODEL", "google/gemma-3-4b")

# ==============================
# 📦 VECTOR DATABASE AYARLARI
# ==============================
VECTOR_DB_PATH = "vectordb"
COLLECTION_NAME = "sales_interview_knowledge"

# ==============================
# ✂️ CHUNK AYARLARI (RAG)
# ==============================
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# ==============================
# 🔍 RETRIEVAL AYARLARI
# ==============================
TOP_K = 3

# ==============================
# 🎯 MÜLAKAT AYARLARI
# ==============================
QUESTION_COUNT = 5
TEMPERATURE_QUESTION = 0.7
TEMPERATURE_EVALUATION = 0.1