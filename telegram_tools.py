import os


def get_images(directory: str):
    return [os.path.join(directory, filename)
            for filename in os.listdir(directory)
            if filename.lower().endswith((".png", ".jpg", ".jpeg"))]


def send_photo_to_channel(bot, photo_path: str, channel_id: str):
    with open(photo_path, "rb") as photo:
        bot.send_photo(chat_id=channel_id, photo=photo)
