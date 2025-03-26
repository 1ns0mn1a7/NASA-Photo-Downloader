import os
import random
from dotenv import load_dotenv
import telegram


def send_photo_to_channel(photo_path: str):
    load_dotenv()
    token = os.getenv("telegram_token")
    channel_id = "@nasaphotosdev"

    bot = telegram.Bot(token=token)

    with open(photo_path, "rb") as photo:
        bot.send_photo(chat_id=channel_id, photo=photo)


def main():
    images_folder = "images"
    images = os.listdir(images_folder)

    if images:
        random_image = random.choice(images)
        image_path = os.path.join(images_folder, random_image)
        send_photo_to_channel(image_path)
    else:
        print("ошибка")


if __name__ == "__main__":
    main()
