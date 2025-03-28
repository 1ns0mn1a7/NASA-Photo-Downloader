import os
import time
import random
import argparse
from dotenv import load_dotenv
import telegram
from telegram_tools import get_images, send_photo_to_channel


def publish_photos(bot, directory: str, interval: int, channel_id: str):
    while True:
        images = get_images(directory)
        if not images:
            time.sleep(interval)
            continue
        random.shuffle(images)
        for image in images:
            send_photo_to_channel(bot, image, channel_id)
            time.sleep(interval)


def main():
    load_dotenv()
    telegram_bot_token = os.getenv("TELEGRAM_TOKEN")
    telegram_channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
    default_interval = int(os.getenv("PUBLISH_INTERVAL", 4 * 60 * 60))

    bot = telegram.Bot(token=telegram_bot_token)

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
        default=default_interval,
        help="Интервал публикации в секундах (по умолчанию 4 часа)."
    )
    arguments = parser.parse_args()

    publish_photos(
        bot,
        arguments.directory,
        arguments.interval,
        telegram_channel_id
    )


if __name__ == "__main__":
    main()
