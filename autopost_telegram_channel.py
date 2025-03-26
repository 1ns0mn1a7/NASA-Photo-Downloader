import os
import time
import random
import argparse
from dotenv import load_dotenv
import telegram


load_dotenv()

TOKEN = os.getenv("telegram_token")
CHANNEL_ID = "@nasaphotosdev"
DEFAULT_INTERVAL = int(os.getenv("PUBLISH_INTERVAL", 4 * 60 * 60))

bot = telegram.Bot(token=TOKEN)


def send_photo_to_channel(photo_path: str):
    with open(photo_path, "rb") as photo:
        bot.send_photo(chat_id=CHANNEL_ID, photo=photo)


def get_images_list(directory: str):
    return [os.path.join(directory, filename)
            for filename in os.listdir(directory)
            if filename.lower().endswith((".png", ".jpg", ".jpeg"))]


def publish_photos(directory: str, interval: int):
    while True:
        images = get_images_list(directory)
        if not images:
            time.sleep(interval)
            continue
        random.shuffle(images)
        for image in images:
            send_photo_to_channel(image)
            time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(
        description="Скрипт для публикации фотографий в Telegram-канал."
        )
    parser.add_argument(
        "--directory",
        type=str,
        default="images",
        help="Папка с изображениями (по умолчанию 'images')."
        )
    parser.add_argument(
        "--interval",
        type=int,
        default=DEFAULT_INTERVAL,
        help="Интервал публикации в секундах (по умолчанию 4 часа)."
        )
    arguments = parser.parse_args()
    publish_photos(arguments.directory, arguments.interval)


if __name__ == "__main__":
    main()
