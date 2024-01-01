import requests
from . import entities
import os
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")


# clean the message for telegram api to avoid errors
def clean_message(message: str) -> str:
    return (
        message.replace(".", "\.")
        .replace("(", "\(")
        .replace(")", "\)")
        .replace("-", "\-")
        .replace("+", "\+")
        .replace("=", "\=")
        .replace("_", "\_")
    )


# send a message to the telegram group
def send_message(message: str, chat_id: str = TELEGRAM_CHANNEL_ID) -> str:
    url = f"https://api.telegram.org/{entities.API_KEY}/sendMessage"

    message = clean_message(message)

    payload = {
        "text": message,
        "parse_mode": "MarkdownV2",
        "chat_id": chat_id,
    }

    headers = {"accept": "application/json", "content-type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    return response.text
