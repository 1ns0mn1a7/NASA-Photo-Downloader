import requests
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os


def get_epic_earth_photo(api_key, folder="images", count=10):
    base_url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": api_key}
    response = requests.get(base_url, params=params, timeout=10)
    data = response.json()

    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    for i, image_data in enumerate(data[:count]):
        date_str = image_data["date"]
        image_name = image_data["image"]

        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        year = date_obj.strftime("%Y")
        month = date_obj.strftime("%m")
        day = date_obj.strftime("%d")

        photo_url = (f"https://api.nasa.gov/EPIC/archive/natural/"
                     f"{year}/{month}/{day}/png/{image_name}.png?"
                     f"api_key={api_key}")

        filename = folder / f"epic_earth_{i}.png"
        img_response = requests.get(photo_url, timeout=10)
        with open(filename, "wb") as file:
            file.write(img_response.content)
        print(f"Скачан файл: {filename}")


def main():
    load_dotenv()
    api_key = os.getenv("api_key")

    parser = argparse.ArgumentParser(
        description="Скачивание изображений Земли NASA EPIC"
        )
    parser.add_argument("--folder",
                        default="images",
                        help="Путь к папке для сохранения"
                        )
    parser.add_argument("--count",
                        type=int,
                        default=10,
                        help="Количество скачиваемых изображений"
                        )

    args = parser.parse_args()
    get_epic_earth_photo(api_key, args.folder, args.count)


if __name__ == "__main__":
    main()
