import requests
import argparse
from pathlib import Path
from download_tools import download_image


def fetch_spacex_launch(launch_id="latest", folder="images"):
    base_url = "https://api.spacexdata.com/v5/launches"
    url = f"{base_url}/{launch_id}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    spacex_images = response.json()

    flickr_urls = (
        spacex_images
        .get("links", {})
        .get("flickr", {})
        .get("original", [])
    )

    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    for index, image_url in enumerate(flickr_urls):
        filename = folder / f"spacex_{index}.jpg"
        download_image(image_url, filename)


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
    try:
        fetch_spacex_launch(arguments.launch_id, arguments.folder)
    except requests.exceptions.RequestException as error:
        print(error)
        raise


if __name__ == "__main__":
    main()
