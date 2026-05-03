from core.loader import load_knowledge
from core.vectorstore import build_vectorstore

text = load_knowledge("data/knowledge/sales_consultant.txt")

build_vectorstore(text, role_name="sales_consultant")