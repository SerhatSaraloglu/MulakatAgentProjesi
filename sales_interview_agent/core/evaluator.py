# core/evaluator.py

import json
import re
from typing import Any

from core.llm_client import ask_llm
from config import TEMPERATURE_EVALUATION


BAD_PATTERNS = [
    r"\bküfür ederim\b",
    r"\balmazsan alma\b",
    r"\bumrumda değil\b",
    r"\bistemiyorsa almasın\b",
    r"\bbeni ilgilendirmez\b",
    r"\bgit başka yerden al\b",
]


def normalize_text(text: str) -> str:
    """
    Metni küçük harfe çevirir ve fazla boşlukları temizler.
    """
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def contains_aggressive_language(answer: str) -> bool:
    """
    Aday cevabında saldırgan / profesyonel olmayan dil var mı kontrol eder.
    """
    normalized = normalize_text(answer)
    return any(re.search(pattern, normalized) for pattern in BAD_PATTERNS)


def safe_json_load(text: str) -> dict[str, Any]:
    """
    Model cevabından JSON bloğunu güvenli şekilde ayıklar.
    """
    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("Geçerli bir JSON bloğu bulunamadı.")

    cleaned = cleaned[start:end + 1]
    return json.loads(cleaned)


def clamp_score(value: Any, min_value: float = 0.0, max_value: float = 10.0) -> float:
    """
    Skoru sayıya çevirir ve belirtilen aralıkta sınırlar.
    """
    try:
        value = float(value)
    except (TypeError, ValueError):
        return min_value

    return max(min_value, min(value, max_value))


def calculate_final_score(s1: float, s2: float, s3: float, s4: float) -> float:
    """
    Kriter skorlarından nihai puanı hesaplar.
    Bazı temel satış becerileri çok düşükse toplam puana tavan uygular.
    """
    avg_score = (s1 + s2 + s3 + s4) / 4

    if s1 < 4 or s2 < 4:
        avg_score = min(avg_score, 5.5)

    if s1 < 3 and s2 < 3:
        avg_score = min(avg_score, 4.5)

    return round(avg_score, 1)


def build_system_prompt() -> str:
    return (
        "Sen deneyimli, adil ve profesyonel bir işe alım uzmanısın. "
        "Satış danışmanı adaylarının cevaplarını gerçek işe uygunluk açısından değerlendirirsin. "
        "Zayıf cevaplara gereğinden yüksek puan vermezsin. "
        "Sadece geçerli JSON döndürürsün."
    )


def build_user_prompt(question: str, answer: str, context: str) -> str:
    return f"""
Soru:
{question}

Adayın cevabı:
{answer}

Referans bağlam:
{context}

Görev:
Adayın cevabını 4 kriter üzerinden değerlendir:

1. empati_ve_musteri_odaklilik
2. ihtiyac_anlama_ve_soru_sorma
3. deger_odakli_aciklama
4. alternatif_ve_cozum_sunma

Değerlendirme kuralları:
- Sadece "ürün kaliteli" demek güçlü bir değer açıklaması sayılmaz
- Müşterinin endişesini anlamadan konuşmak empati sayılmaz
- "İsterse alır, istemezse almaz" gibi yaklaşım müşteri odaklı güçlü bir satış yaklaşımı değildir
- Alternatif sunma yüzeysel geçiyorsa yüksek puan verme
- Temel satış mantığı yoksa 7 ve üzeri puan verme
- Hakaret, küfür, saldırgan veya küçümseyici dil varsa puan çok düşük olmalıdır
- Gerçekten güçlü olmayan cevaplara yüksek puan yazma

Aşağıdaki örnekleri referans al:

ÖRNEK GÜÇLÜ CEVAP:
"Müşterinin fiyat konusundaki endişesini önce dikkatle dinler ve empati kurarım. Ardından ürünün uzun vadeli faydalarını ve neden bu fiyatı hak ettiğini açıklarım. Gerekirse müşterinin bütçesine uygun alternatif ürünler, kampanya ya da taksit seçenekleri sunarım. Amacım baskı yapmak değil, müşteriye en doğru çözümü sunmaktır."

ÖRNEK GÜÇLÜ CEVAP JSON:
{{
  "empati_ve_musteri_odaklilik": 9,
  "ihtiyac_anlama_ve_soru_sorma": 8,
  "deger_odakli_aciklama": 9,
  "alternatif_ve_cozum_sunma": 9,
  "guclu_yonler": [
    "Müşteri endişesini anlayan empatik bir yaklaşım var",
    "Değer odaklı açıklama ve çözüm üretme güçlü"
  ],
  "eksik_yonler": [
    "Daha somut bir müşteri örneği eklenebilirdi"
  ],
  "gelistirme_onerisi": "Cevap gerçek bir mağaza senaryosu ile desteklenirse daha da güçlenir."
}}

ÖRNEK ORTA CEVAP:
"Müşteriyi dinlerim ve ürünün kaliteli olduğunu söylerim. Gerekirse başka ürünler de gösterebilirim."

ÖRNEK ORTA CEVAP JSON:
{{
  "empati_ve_musteri_odaklilik": 6,
  "ihtiyac_anlama_ve_soru_sorma": 4,
  "deger_odakli_aciklama": 5,
  "alternatif_ve_cozum_sunma": 6,
  "guclu_yonler": [
    "Müşteriyi dinleme yaklaşımı mevcut",
    "Alternatif sunma niyeti var"
  ],
  "eksik_yonler": [
    "Cevap yüzeysel kalmış",
    "Değer açıklaması güçlü değil"
  ],
  "gelistirme_onerisi": "Müşterinin ihtiyacını anlamaya yönelik daha net bir yaklaşım eklenmeli."
}}

ÖRNEK ZAYIF CEVAP:
"Fiyat normal. İsterse alır istemezse almaz. Kaliteli ürün zaten."

ÖRNEK ZAYIF CEVAP JSON:
{{
  "empati_ve_musteri_odaklilik": 2,
  "ihtiyac_anlama_ve_soru_sorma": 1,
  "deger_odakli_aciklama": 3,
  "alternatif_ve_cozum_sunma": 2,
  "guclu_yonler": [
    "Ürünün kaliteli olduğunu vurgulama çabası var"
  ],
  "eksik_yonler": [
    "Empati yok",
    "Müşteri ihtiyacını anlamaya yönelik yaklaşım yok",
    "Müşteri odaklı çözüm zayıf"
  ],
  "gelistirme_onerisi": "Müşterinin endişesini anlayan ve çözüm sunan bir yaklaşım benimsenmeli."
}}

ÖRNEK ÇOK ZAYIF CEVAP:
"Küfür ederim, almazsan alma derim."

ÖRNEK ÇOK ZAYIF CEVAP JSON:
{{
  "empati_ve_musteri_odaklilik": 0,
  "ihtiyac_anlama_ve_soru_sorma": 0,
  "deger_odakli_aciklama": 0,
  "alternatif_ve_cozum_sunma": 0,
  "guclu_yonler": [
    "Belirgin bir güçlü yön yok"
  ],
  "eksik_yonler": [
    "Profesyonellik yok",
    "Müşteri odaklı yaklaşım yok",
    "Saldırgan ve uygunsuz dil kullanılmış"
  ],
  "gelistirme_onerisi": "Müşterilere saygılı, sakin ve çözüm odaklı yaklaşım benimsenmelidir."
}}

Sadece şu formatta JSON döndür:
{{
  "empati_ve_musteri_odaklilik": 0,
  "ihtiyac_anlama_ve_soru_sorma": 0,
  "deger_odakli_aciklama": 0,
  "alternatif_ve_cozum_sunma": 0,
  "guclu_yonler": ["...", "..."],
  "eksik_yonler": ["...", "..."],
  "gelistirme_onerisi": "..."
}}
"""


def build_hard_fail_feedback() -> tuple[str, float]:
    """
    Sert kural ihlali durumunda dönecek sabit cevap.
    """
    feedback = (
        "Güçlü Yönler:\n"
        "- Belirgin bir güçlü yön bulunmuyor.\n"
        "\nEksik Yönler:\n"
        "- Profesyonel olmayan ve saldırgan bir ifade kullanılmış.\n"
        "- Müşteri odaklı yaklaşım bulunmuyor.\n"
        "- Empati, çözüm üretme ve satış becerisi gösterilmiyor.\n"
        "\nGeliştirme Önerisi:\n"
        "- Müşteri itirazlarına sakin, saygılı ve çözüm odaklı yaklaşılmalıdır.\n"
        "\nKriter Bazlı Puanlar:\n"
        "- Empati ve müşteri odaklılık: 0/10\n"
        "- İhtiyacı anlama ve soru sorma: 0/10\n"
        "- Değer odaklı açıklama: 0/10\n"
        "- Alternatif ve çözüm sunma: 0/10\n"
        "\nPuan:\n"
        "0.5/10"
    )
    return feedback, 0.5


def build_result_dict(data: dict[str, Any]) -> dict[str, Any]:
    """
    LLM çıktısını normalize eder ve nihai skorları üretir.
    """
    s1 = clamp_score(data.get("empati_ve_musteri_odaklilik", 0))
    s2 = clamp_score(data.get("ihtiyac_anlama_ve_soru_sorma", 0))
    s3 = clamp_score(data.get("deger_odakli_aciklama", 0))
    s4 = clamp_score(data.get("alternatif_ve_cozum_sunma", 0))

    final_score = calculate_final_score(s1, s2, s3, s4)

    guclu_yonler = data.get("guclu_yonler", [])
    eksik_yonler = data.get("eksik_yonler", [])
    gelistirme_onerisi = data.get("gelistirme_onerisi", "")

    if not isinstance(guclu_yonler, list):
        guclu_yonler = []
    if not isinstance(eksik_yonler, list):
        eksik_yonler = []
    if not isinstance(gelistirme_onerisi, str):
        gelistirme_onerisi = ""

    return {
        "scores": {
            "empati_ve_musteri_odaklilik": s1,
            "ihtiyac_anlama_ve_soru_sorma": s2,
            "deger_odakli_aciklama": s3,
            "alternatif_ve_cozum_sunma": s4,
        },
        "score": final_score,
        "guclu_yonler": guclu_yonler,
        "eksik_yonler": eksik_yonler,
        "gelistirme_onerisi": gelistirme_onerisi,
    }


def format_feedback(result: dict[str, Any]) -> str:
    """
    Yapısal sonucu kullanıcıya gösterilecek metne çevirir.
    """
    scores = result["scores"]
    guclu_yonler = result["guclu_yonler"]
    eksik_yonler = result["eksik_yonler"]
    gelistirme_onerisi = result["gelistirme_onerisi"]
    final_score = result["score"]

    feedback_lines = []

    feedback_lines.append("Güçlü Yönler:")
    if guclu_yonler:
        for item in guclu_yonler:
            feedback_lines.append(f"- {item}")
    else:
        feedback_lines.append("- Belirgin bir güçlü yön belirtilmedi.")

    feedback_lines.append("\nEksik Yönler:")
    if eksik_yonler:
        for item in eksik_yonler:
            feedback_lines.append(f"- {item}")
    else:
        feedback_lines.append("- Belirgin bir eksik yön belirtilmedi.")

    feedback_lines.append("\nGeliştirme Önerisi:")
    if gelistirme_onerisi:
        feedback_lines.append(f"- {gelistirme_onerisi}")
    else:
        feedback_lines.append("- Daha somut ve müşteri odaklı bir yaklaşım anlatılabilir.")

    feedback_lines.append("\nKriter Bazlı Puanlar:")
    feedback_lines.append(
        f"- Empati ve müşteri odaklılık: {scores['empati_ve_musteri_odaklilik']}/10"
    )
    feedback_lines.append(
        f"- İhtiyacı anlama ve soru sorma: {scores['ihtiyac_anlama_ve_soru_sorma']}/10"
    )
    feedback_lines.append(
        f"- Değer odaklı açıklama: {scores['deger_odakli_aciklama']}/10"
    )
    feedback_lines.append(
        f"- Alternatif ve çözüm sunma: {scores['alternatif_ve_cozum_sunma']}/10"
    )

    feedback_lines.append(f"\nPuan:\n{final_score}/10")

    return "\n".join(feedback_lines)


def build_fallback_feedback(reason: str = "") -> tuple[str, float]:
    """
    LLM çıktısı bozulduğunda veya parse edilemediğinde kullanılacak güvenli dönüş.
    """
    detail = f"- Teknik neden: {reason}\n" if reason else ""

    feedback = (
        "Güçlü Yönler:\n"
        "- Değerlendirme üretilemediği için güçlü yönler çıkarılamadı.\n"
        "\nEksik Yönler:\n"
        "- Model çıktısı beklenen formatta alınamadı.\n"
        f"{detail}"
        "\nGeliştirme Önerisi:\n"
        "- Aynı cevap yeniden değerlendirilebilir veya JSON çıktısı daha sıkı zorlanabilir.\n"
        "\nPuan:\n"
        "3.0/10"
    )
    return feedback, 3.0


def evaluate_answer(question: str, answer: str, context: str) -> tuple[str, float]:
    """
    Aday cevabını değerlendirir ve (feedback, score) döner.
    """

    if contains_aggressive_language(answer):
        return build_hard_fail_feedback()

    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(question, answer, context)

    raw_response = ask_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=TEMPERATURE_EVALUATION,
        max_tokens=700
    )

    try:
        data = safe_json_load(raw_response)
        result = build_result_dict(data)
        feedback = format_feedback(result)
        return feedback, result["score"]

    except json.JSONDecodeError:
        return build_fallback_feedback("JSON ayrıştırılamadı")

    except ValueError as e:
        return build_fallback_feedback(str(e))

    except Exception:
        return build_fallback_feedback("Beklenmeyen bir hata oluştu")