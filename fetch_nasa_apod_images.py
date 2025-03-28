import requests
import argparse
from pathlib import Path
from dotenv import load_dotenv
import os
from url_get_file_extension import get_file_extension
from download_tools import download_image


def fetch_nasa_apod(api_key, folder="images", count=50):
    base_url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": api_key,
        "count": count
    }

    response = requests.get(base_url, params=params, timeout=10)
    response.raise_for_status()
    apod_entries = response.json()

    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    for index, apod_entry in enumerate(apod_entries):
        if apod_entry.get("media_type") != "image":
            continue

        image_url = apod_entry["url"]
        extension = get_file_extension(image_url)
        filename = folder / f"nasa_apod_{index}{extension}"

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
    try:
        fetch_nasa_apod(api_key, arguments.folder, arguments.count)
    except requests.exceptions.RequestException as error:
        print(error)
        raise


if __name__ == "__main__":
    main()
