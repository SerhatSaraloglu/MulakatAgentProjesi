from core.evaluator import evaluate_answer

question = "Müşteri bir ürünün pahalı olduğunu söylerse nasıl yaklaşırsınız?"

answer = """
Önce müşteriyi dikkatlice dinlerim. Neden pahalı bulduğunu anlamaya çalışırım.
Sonra ürünün avantajlarını ve müşteriye sağlayacağı faydayı anlatırım.
Gerekirse alternatif ürün de sunarım.
"""

context = """
İtiraz Yönetimi:
Müşteri fiyat, kalite veya ihtiyaç konusunda itiraz edebilir.
Bu durumda müşteriyi dinlemek, empati kurmak, alternatif sunmak ve ürünün değerini anlatmak gerekir.
"""

result = evaluate_answer(question, answer, context)

print("DEĞERLENDİRME:\n")
print(result)