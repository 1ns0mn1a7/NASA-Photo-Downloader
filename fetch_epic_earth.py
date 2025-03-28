import requests
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os
from urllib.parse import urlencode


def download_image(url, filename):
    try:
        img_response = requests.get(url, timeout=10)
        img_response.raise_for_status()
        with open(filename, "wb") as file:
            file.write(img_response.content)
    except requests.exceptions.RequestException as error:
        print(f"Ошибка при скачивании {url}: {error}")


def get_epic_earth_photo(api_key, folder="images", count=10):
    base_url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": api_key}

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        epic_images = response.json()
    except requests.exceptions.RequestException as error:
        print(f"Ошибка при запросе к NASA EPIC API: {error}")
        return

    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    for image_index, image_data in enumerate(epic_images[:count]):
        date_str = image_data["date"]
        image_name = image_data["image"]

        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        year = date_obj.strftime("%Y")
        month = date_obj.strftime("%m")
        day = date_obj.strftime("%d")

        photo_base_url = (
            f"https://api.nasa.gov/EPIC/archive/natural/"
            f"{year}/{month}/{day}/png/{image_name}.png"
        )
        photo_params = {"api_key": api_key}
        photo_url = f"{photo_base_url}?{urlencode(photo_params)}"
        filename = folder / f"epic_earth_{image_index}.png"

        download_image(photo_url, filename)


def main():
    load_dotenv()
    api_key = os.getenv("NASA_API_KEY")

    parser = argparse.ArgumentParser(
        description="Скачивание изображений Земли NASA EPIC"
    )
    parser.add_argument(
        "--folder",
        default="images",
        help="Путь к папке для сохранения"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Количество скачиваемых изображений"
    )

    arguments = parser.parse_args()
    get_epic_earth_photo(api_key, arguments.folder, arguments.count)


if __name__ == "__main__":
    main()
