import os
from dotenv import load_dotenv
import telegram


def send_message_to_channel(message: str):
    load_dotenv()
    token = os.getenv("telegram_token")
    channel_id = "@nasaphotosdev"

    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=channel_id, text=message)


def main():
    message_text = "test"
    send_message_to_channel(message_text)


if __name__ == "__main__":
    main()
