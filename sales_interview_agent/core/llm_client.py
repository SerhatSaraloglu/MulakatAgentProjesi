# core/llm_client.py

from openai import OpenAI
from config import (
    LM_STUDIO_BASE_URL,
    LM_STUDIO_API_KEY,
    LLM_MODEL
)

client = OpenAI(
    base_url=LM_STUDIO_BASE_URL,
    api_key=LM_STUDIO_API_KEY
)


def ask_llm(system_prompt: str, user_prompt: str, temperature: float = 0.7, max_tokens: int = 400) -> str:
    """
    LM Studio üzerindeki modele istek atar ve yanıtı döner
    """
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )

    return response.choices[0].message.content.strip()