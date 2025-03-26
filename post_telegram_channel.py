import os
import random
import argparse
from dotenv import load_dotenv
import telegram


load_dotenv()

TOKEN = os.getenv("telegram_token")
CHANNEL_ID = "@nasaphotosdev"

bot = telegram.Bot(token=TOKEN)


def send_photo_to_channel(photo_path: str):
    with open(photo_path, "rb") as photo:
        bot.send_photo(chat_id=CHANNEL_ID, photo=photo)


def get_images_list(directory: str):
    return [os.path.join(directory, filename)
            for filename in os.listdir(directory)
            if filename.lower().endswith((".png", ".jpg", ".jpeg"))]


def publish_photo(directory: str, choose_photo: str = None):
    images = get_images_list(directory)

    if choose_photo:
        choose_photo_path = os.path.join(directory, choose_photo)
        if choose_photo_path in images:
            send_photo_to_channel(choose_photo_path)
    else:
        if images:
            random_image = random.choice(images)
            send_photo_to_channel(random_image)


def main():
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
    publish_photo(arguments.directory, arguments.photo)


if __name__ == "__main__":
    main()
