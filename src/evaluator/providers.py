import os
from openai import OpenAI

from src.config import MODEL_NAME

def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set")

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("openai package is not installed") from exc

    return OpenAI(api_key=api_key)



def call_openai(system_prompt: str, user_prompt: str, model: str = MODEL_NAME) -> str:
    client = get_openai_client()

    response = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    content = response.choices[0].message.content
    if not content:
        raise ValueError("OpenAI response content is empty")

    return content