# app.py

import random

from core.loader import load_roles, load_knowledge
from core.vectorstore import build_vectorstore
from core.retriever import retrieve_context
from core.question_generator import generate_question
from core.evaluator import evaluate_answer
from config import QUESTION_COUNT


def generate_final_report(role_title: str, results: list[dict]) -> str:
    """
    Mülakat sonunda genel rapor oluşturur.
    """
    total_score = sum(item["score"] for item in results)
    average_score = total_score / len(results) if results else 0

    strong_topics = []
    weak_topics = []

    for item in results:
        if item["score"] >= 8:
            strong_topics.append(item["topic"])
        elif item["score"] <= 5:
            weak_topics.append(item["topic"])

    report = []
    report.append("\n=== GENEL MÜLAKAT RAPORU ===")
    report.append(f"Rol: {role_title}")
    report.append(f"Toplam Soru Sayısı: {len(results)}")
    report.append(f"Toplam Puan: {total_score}/{len(results) * 10}")
    report.append(f"Ortalama Puan: {average_score:.2f}/10")

    if average_score >= 8:
        genel_durum = "Aday genel olarak güçlü bir performans gösterdi."
    elif average_score >= 6:
        genel_durum = "Aday orta seviyede bir performans gösterdi."
    else:
        genel_durum = "Adayın geliştirmesi gereken önemli alanlar bulunuyor."

    report.append(f"Genel Değerlendirme: {genel_durum}")

    report.append("\nGüçlü Olduğu Konular:")
    if strong_topics:
        for topic in strong_topics:
            report.append(f"- {topic}")
    else:
        report.append("- Belirgin şekilde öne çıkan bir konu yok.")

    report.append("\nGeliştirilmesi Gereken Konular:")
    if weak_topics:
        for topic in weak_topics:
            report.append(f"- {topic}")
    else:
        report.append("- Kritik seviyede zayıf görünen bir konu yok.")

    return "\n".join(report)


def main():
    print("=== Satış Danışmanı Mülakat Agentı ===\n")

    # 1. Rol bilgilerini yükle
    roles = load_roles("data/roles.json")
    role_key = "sales_consultant"
    role = roles[role_key]

    print(f"Rol: {role['title']}")
    print(f"Açıklama: {role['description']}\n")

    # 2. Knowledge dosyasını yükle
    knowledge_path = f"data/knowledge/{role['knowledge_file']}"
    knowledge_text = load_knowledge(knowledge_path)

    # 3. Vector DB oluştur
    print("Bilgi tabanı hazırlanıyor...")
    build_vectorstore(knowledge_text, role_name=role_key)
    print("Bilgi tabanı hazır.\n")

    # 4. Topic listesini al
    topics = role["topics"].copy()
    random.shuffle(topics)

    results = []
    asked_count = 0

    # 5. Mülakat döngüsü
    for topic in topics[:QUESTION_COUNT]:
        asked_count += 1

        print(f"\n--- Soru {asked_count} / {QUESTION_COUNT} ---")
        print(f"Konu: {topic}")

        # 5.1 Context çek
        context = retrieve_context(topic, role_name=role_key)

        # 5.2 Soru üret
        question = generate_question(
            role_title=role["title"],
            topic=topic,
            context=context
        )

        print(f"\nSoru: {question}")
        answer = input("\nCevabın: ")

        # 5.3 Değerlendirme
        print("\nCevap değerlendiriliyor...\n")
        feedback, score = evaluate_answer(
            question=question,
            answer=answer,
            context=context
        )

        print("Değerlendirme:")
        print(feedback)
        print(f"\nBu sorunun puanı: {score}/10")
        print("\n" + "=" * 50)

        results.append({
            "topic": topic,
            "question": question,
            "answer": answer,
            "feedback": feedback,
            "score": score
        })

    # 6. Genel rapor
    final_report = generate_final_report(role["title"], results)
    print(final_report)


if __name__ == "__main__":
    main()