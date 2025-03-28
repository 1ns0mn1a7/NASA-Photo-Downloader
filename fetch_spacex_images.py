import requests
import argparse
from pathlib import Path


def download_image(link, filename):
    try:
        img_response = requests.get(link, timeout=10)
        img_response.raise_for_status()
        with open(filename, "wb") as file:
            file.write(img_response.content)
    except requests.exceptions.RequestException as error:
        print(f"Ошибка при скачивании {link}: {error}")


def fetch_spacex_launch(launch_id=None, folder="images"):
    base_url = "https://api.spacexdata.com/v5/launches"
    url = f"{base_url}/{launch_id}" if launch_id else f"{base_url}/latest"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        spacex_images = response.json()

        flickr_links = (
            spacex_images
            .get("links", {})
            .get("flickr", {})
            .get("original", [])
        )
    except requests.exceptions.RequestException as error:
        print(f"Ошибка при запросе к NASA APOD API: {error}")
        return

    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    for number, link in enumerate(flickr_links):
        filename = folder / f"spacex_{number}.jpg"
        download_image(link, filename)


def main():
    parser = argparse.ArgumentParser(
        description="Скачивание изображений запусков SpaceX"
    )
    parser.add_argument(
        "--launch-id",
        default="latest",
        help="ID конкретного запуска SpaceX"
    )
    parser.add_argument(
        "--folder",
        default="images",
        help="Путь к папке для сохранения"
    )

    arguments = parser.parse_args()
    fetch_spacex_launch(arguments.launch_id, arguments.folder)


if __name__ == "__main__":
    main()
