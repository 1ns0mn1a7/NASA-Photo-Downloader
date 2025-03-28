import os
import random
import argparse
from dotenv import load_dotenv
import telegram
from telegram_tools import get_images, send_photo_to_channel


def publish_photo(
        bot,
        directory: str,
        channel_id: str,
        choose_photo: str = None
):
    images = get_images(directory)

    if choose_photo:
        choose_photo_path = os.path.join(directory, choose_photo)
        if choose_photo_path in images:
            send_photo_to_channel(bot, choose_photo_path, channel_id)
    else:
        if images:
            random_image = random.choice(images)
            send_photo_to_channel(bot, random_image, channel_id)


def main():
    load_dotenv()
    telegram_bot_token = os.getenv("TELEGRAM_TOKEN")
    telegram_channel_id = os.getenv("TELEGRAM_CHANNEL_ID")

    bot = telegram.Bot(token=telegram_bot_token)

    parser = argparse.ArgumentParser(
        description="Скрипт для публикации фотографии в Telegram-канал."
    )
    parser.add_argument(
        "--directory",
        type=str,
        default="images",
        help="Папка с изображениями (по умолчанию 'images')."
    )
    parser.add_argument(
        "--photo",
        type=str,
        help="Название фотографии для публикации "
             "(если не указано, публикуется случайная)."
    )
    arguments = parser.parse_args()

    publish_photo(
        bot,
        arguments.directory,
        telegram_channel_id,
        arguments.photo
    )


if __name__ == "__main__":
    main()
