import requests
import argparse
from pathlib import Path
from dotenv import load_dotenv
import os
from url_get_file_extension import get_file_extension


def fetch_nasa_apod(api_key, folder="images", count=50):
    base_url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": api_key,
        "count": count
    }
    response = requests.get(base_url, params=params, timeout=10)
    data = response.json()

    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    for number, item in enumerate(data):
        if item.get("media_type") == "image":
            image_url = item["url"]
            extension = get_file_extension(image_url)

            filename = folder / f"nasa_apod_{number}{extension}"
            img_response = requests.get(image_url, timeout=10)
            with open(filename, "wb") as file:
                file.write(img_response.content)
            print(f"Скачан файл: {filename}")


def main():
    load_dotenv()
    api_key = os.getenv("api_key")

    parser = argparse.ArgumentParser(
        description="Скачивание изображений NASA APOD"
        )
    parser.add_argument("--folder",
                        default="images",
                        help="Путь к папке для сохранения"
                        )
    parser.add_argument("--count",
                        type=int,
                        default=50,
                        help="Количество скачиваемых изображений"
                        )

    args = parser.parse_args()
    fetch_nasa_apod(api_key, args.folder, args.count)


if __name__ == "__main__":
    main()
