import logging

import requests

def send_telegram_message(bot_token, chat_id, message):
    """Sends a message via Telegram bot."""
    logging.info(f"📤 Sending Telegram message: {message}")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "disable_notification": False}

    try:
        response = requests.post(url, json=payload)
        if response.json().get("ok"):
            logging.info("✅ Telegram message sent successfully.")
        else:
            logging.error(f"❌ Telegram API error: {response.json()}")
    except requests.RequestException as e:
        logging.error(f"🚨 Failed to send Telegram message: {e}")
