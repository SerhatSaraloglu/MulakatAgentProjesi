from core.retriever import retrieve_context
from core.question_generator import generate_question

topic = "itiraz yönetimi"
context = retrieve_context(topic, role_name="sales_consultant")

question = generate_question(
    role_title="Satış Danışmanı",
    topic=topic,
    context=context
)

print("Üretilen soru:\n")
print(question)