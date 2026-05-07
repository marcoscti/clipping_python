import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


def enviar_telegram(mensagem):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": mensagem
        }
    )
