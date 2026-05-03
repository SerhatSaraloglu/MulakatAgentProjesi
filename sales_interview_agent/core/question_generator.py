# core/question_generator.py

from core.llm_client import ask_llm
from config import TEMPERATURE_QUESTION


def clean_question_output(text: str) -> str:
    """
    Model çıktısını temizler.
    """
    text = text.strip()

    if text.startswith("Soru:"):
        text = text.replace("Soru:", "", 1).strip()

    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1].strip()

    return text


def generate_question(role_title: str, topic: str, context: str) -> str:
    """
    Verilen rol, konu ve bağlama göre tek bir mülakat sorusu üretir.
    Soru, topic ile birebir uyumlu olmak zorundadır.
    """

    system_prompt = (
        "Sen profesyonel bir işe alım uzmanısın. "
        "Satış danışmanı adayı için gerçekçi, kısa, net ve konuya birebir uygun mülakat soruları üretirsin. "
        "Seçilen konudan asla sapmazsın."
    )

    user_prompt = f"""
Rol: {role_title}
Konu: {topic}

Bağlam:
{context}

Görev:
Yukarıdaki rol, konu ve bağlama göre satış danışmanı adayı için sadece 1 adet mülakat sorusu üret.

Zorunlu kurallar:
- Soru yalnızca verilen "Konu"yu ölçmelidir
- Konu ile soru birebir anlam uyumlu olmalıdır
- Başka bir satış becerisine kaymamalıdır
- Soru kısa ve net olmalıdır
- Gerçek iş hayatına uygun olmalıdır
- Tek soru üretilmelidir
- Açıklama eklenmemelidir
- Cevabında sadece soru cümlesi yer almalıdır

Konuya uyum örnekleri:
- Konu "müşteri karşılama" ise soru; müşteriyi karşılama, ilk temas, selamlama, ihtiyaç sorma ile ilgili olmalıdır
- Konu "fiyat itirazı" ise soru; müşterinin pahalı bulması, daha ucuz alternatif söylemesi, fiyat karşılaştırması gibi durumlarla ilgili olabilir
- Konu "ürün tanıtımı" ise soru; ürünün faydasını anlatma ile ilgili olmalıdır

Kritik yasak:
- Konu "müşteri karşılama" ise fiyat itirazı, satış kapama, pazarlık, kampanya önerisi veya ürünün pahalı bulunmasıyla ilgili soru üretme
- Konu dışına çıkan soru üretme

Sadece soru cümlesini yaz.
"""

    raw_question = ask_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=TEMPERATURE_QUESTION,
        max_tokens=120
    )

    return clean_question_output(raw_question)