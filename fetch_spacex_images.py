import requests
import argparse
from pathlib import Path


def fetch_spacex_launch(launch_id=None, folder="images"):
    base_url = "https://api.spacexdata.com/v5/launches"
    url = f"{base_url}/{launch_id}" if launch_id else f"{base_url}/latest"

    response = requests.get(url, timeout=10)
    data = response.json()
    flickr_links = data.get("links", {}).get("flickr", {}).get("original", [])

    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    for number, link in enumerate(flickr_links):
        filename = folder / f"spacex_{number}.jpg"
        img_response = requests.get(link, timeout=10)
        with open(filename, 'wb') as file:
            file.write(img_response.content)
        print(f"Скачан файл: {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Скачивание изображений запусков SpaceX"
        )
    parser.add_argument("--launch-id",
                        help="ID конкретного запуска SpaceX"
                        )
    parser.add_argument("--folder",
                        default="images",
                        help="Путь к папке для сохранения"
                        )

    args = parser.parse_args()
    fetch_spacex_launch(args.launch_id, args.folder)


if __name__ == "__main__":
    main()
