from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def gerar_resumo(texto):
    if not OPENAI_API_KEY or client is None:
        return "Resumo por IA desativado"

    resposta = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "Resuma notícias em até 3 linhas."
            },
            {
                "role": "user",
                "content": texto
            }
        ]
    )

    return resposta.choices[0].message.content
