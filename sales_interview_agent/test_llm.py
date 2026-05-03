from core.llm_client import ask_llm

response = ask_llm(
    system_prompt="Sen yardımcı bir asistansın.",
    user_prompt="Bana satış danışmanı mülakatı için kısa bir soru yaz.",
    temperature=0.5,
    max_tokens=100
)

print(response)