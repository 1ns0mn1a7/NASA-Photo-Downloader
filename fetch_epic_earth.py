import requests
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os
from urllib.parse import urlencode
from download_tools import download_image


def get_epic_earth_photo(api_key, folder="images", count=10):
    base_url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": api_key}

    response = requests.get(base_url, params=params, timeout=10)
    response.raise_for_status()
    epic_entries = response.json()

    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    for index, epic_entry in enumerate(epic_entries[:count]):
        date = epic_entry["date"]
        image_name = epic_entry["image"]

        parsed_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        year = parsed_date.strftime("%Y")
        month = parsed_date.strftime("%m")
        day = parsed_date.strftime("%d")

        photo_base_url = (
            f"https://api.nasa.gov/EPIC/archive/natural/"
            f"{year}/{month}/{day}/png/{image_name}.png"
        )
        photo_params = {"api_key": api_key}
        photo_url = f"{photo_base_url}?{urlencode(photo_params)}"
        filename = folder / f"epic_earth_{index}.png"

        download_image(photo_url, filename)


def main():
    load_dotenv()
    api_key = os.getenv("NASA_API_KEY")
    if not api_key:
        print("Ошибка: NASA_API_KEY не задан в переменных окружения.")
        print("Укажите ключ в файле .env или переменной окружения.")
        return

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
    try:
        get_epic_earth_photo(api_key, arguments.folder, arguments.count)
    except requests.exceptions.RequestException as error:
        print(error)
        raise


if __name__ == "__main__":
    main()
