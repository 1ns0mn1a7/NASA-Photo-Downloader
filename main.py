import requests
from datetime import datetime
from urllib.parse import urlsplit, unquote, urlencode
from os.path import split, splitext
from pathlib import Path
from dotenv import load_dotenv
import os


def fetch_spacex_last_launch(launch_id, folder):
    url = f"https://api.spacexdata.com/v5/launches/{launch_id}"

    response = requests.get(url, timeout=10)
    data = response.json()
    flickr_links = data.get("links", {}).get("flickr", {}).get("original", [])

    folder.mkdir(parents=True, exist_ok=True)

    for number, link in enumerate(flickr_links):
        filename = folder / f"spacex_{number}.jpg"
        img_response = requests.get(link, timeout=10)
        with open(filename, 'wb') as file:
            file.write(img_response.content)
        print(f"Скачан файл: {filename}")


def get_file_extension(url):
    parsed_url = urlsplit(url)
    path = unquote(parsed_url.path)
    _, filename = split(path)
    _, extension = splitext(filename)
    return extension


def fetch_nasa_apod(api_key, folder):
    base_url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": api_key,
        "count": 50
    }
    url = f"{base_url}?{urlencode(params)}"

    response = requests.get(url, timeout=10)
    data = response.json()

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


def get_epic_earth_photo(api_key, folder, count=10):
    base_url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": api_key}
    response = requests.get(base_url, params=params, timeout=10)
    data = response.json()

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

    images_folder = Path("images")

    get_epic_earth_photo(api_key, images_folder, count=10)
    launch_id = "5eb87d47ffd86e000604b38a"
    fetch_spacex_last_launch(launch_id, images_folder)
    fetch_nasa_apod(api_key, images_folder)


if __name__ == "__main__":
    main()
