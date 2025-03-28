import requests
import argparse
from pathlib import Path
from dotenv import load_dotenv
import os
from url_get_file_extension import get_file_extension


def download_image(url, filename):
    try:
        img_response = requests.get(url, timeout=10)
        img_response.raise_for_status()
        with open(filename, "wb") as file:
            file.write(img_response.content)
    except requests.exceptions.RequestException as error:
        print(f"Ошибка при скачивании {url}: {error}")


def fetch_nasa_apod(api_key, folder="images", count=50):
    base_url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": api_key,
        "count": count
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        apod_images = response.json()
    except requests.exceptions.RequestException as error:
        print(f"Ошибка при запросе к NASA APOD API: {error}")
        return

    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    for number, item in enumerate(apod_images):
        if item.get("media_type") != "image":
            continue

        image_url = item["url"]
        extension = get_file_extension(image_url)
        filename = folder / f"nasa_apod_{number}{extension}"

        download_image(image_url, filename)


def main():
    load_dotenv()
    api_key = os.getenv("NASA_API_KEY")

    parser = argparse.ArgumentParser(
        description="Скачивание изображений NASA APOD"
    )
    parser.add_argument(
        "--folder",
        default="images",
        help="Путь к папке для сохранения"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=50,
        help="Количество скачиваемых изображений"
    )

    arguments = parser.parse_args()
    fetch_nasa_apod(api_key, arguments.folder, arguments.count)


if __name__ == "__main__":
    main()
