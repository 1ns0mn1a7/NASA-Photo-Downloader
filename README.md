# Космический Телеграм

**Космический Телеграм** — это Python-скрипт, предназначенный для автоматической загрузки и отправки фотографий космоса в Telegram-канал. 
Для получения изображений он использует API NASA и SpaceX.

## Как установить

### Предварительные требования:
    
* Установленный Python 3.8 или выше.
* API-ключ NASA.
* Бот и его токен Telegram.

### Установка зависимостей:

1. **Клонируйте репозиторий:**

```bash
    git clone https://github.com/1ns0mn1a7/NASA-Photo-Downloader.git
    cd NASA-Photo-Downloader
```
    
2. **Создайте и активируйте виртуальное окружение:**
* Для Windows:

```bash
python -m venv env
env\Scripts\activate
```

* Для macOS/Linux:

```bash
python3 -m venv env
source env/bin/activate
```

3. **Установите необходимые зависимости:**

```bash
pip install -r requirements.txt
```

### Настройки параметров окружения
Для работы скрипта необходимо настроить файл .env со следующими параметрами:
* `NASA_API_KEY` - ваш ключ [NASA API](https://api.nasa.gov/).
* `TELEGRAM_TOKEN` - токен вашего Telegram-бота. Получите его у [BotFather](https://core.telegram.org/bots#botfather) и следуйте инструкциям для создания нового бота.
* `TELEGRAM_CHANNEL_ID` - идентификатор Telegram-канала, куда будут отправляться фото. Это ссылка на него, например: `@example`.

## Примеры запуска скриптов
### `autopost_telegram_channel.py` - скрипт для автоматической загрузки фотографий в Telegram-канал.
Скрипт поддерживает аргументы командной строки для настройки выбора папки с изображениями и интервала публикации.

* По умолчанию:
```bash
python autopost_telegram_channel.py
```

* Выбрать папку (например, `photos`):
```bash
python autopost_telegram_channel.py --directory photos
```

* Выбрать интервал (например, 1 час = 3600 сек):
```bash
python autopost_telegram_channel.py --interval 3600
```

* Комбинированно (папка `space`, интервал 2 часа):
```bash
python autopost_telegram_channel.py --directory space_images --interval 7200
```

### `post_telegram_channel.py` - скрипт для публикации одной фотографии в Telegram-канал.
Скрипт публикует случайное фото или указанное по имени из заданной папки.

* По умолчанию:
```bash
python post_telegram_channel.py
```

* Выбрать папку (например, `photos`):
```bash
python post_telegram_channel.py --directory photos
```

* Указать фото (например, `space.jpg`):
```bash
python post_telegram_channel.py --photo space.jpg
```

* Комбинированно (папка `space`, фото `mars.png`):
```bash
python post_telegram_channel.py --directory space_images --interval 7200
```

### `fetch_epic_earth.py` - скрипт для скачивания изображений Земли с NASA EPIC.
Скрипт загружает фото Земли из архива NASA EPIC в указанную папку.

* По умолчанию (10 фото в `images`):
```bash
python fetch_epic_earth.py
```

* Выбрать папку (например, `earth`):
```bash
python fetch_epic_earth.py --folder earth
```

* Указать количество (например, 5 фото):
```bash
python fetch_epic_earth.py --count 5
```

* Комбинированно (папка `earth`, 3 фото):
```bash
python fetch_epic_earth.py --folder earth --count 3
```

### `fetch_nasa_apod_images.py` - скрипт для скачивания изображений NASA APOD.
Скрипт загружает фото дня NASA APOD в указанную папку.

* По умолчанию (50 фото в `images`):
```bash
python fetch_nasa_apod_images.py
```

* Выбрать папку (например, `apod`):
```bash
python fetch_nasa_apod_images.py --folder apod
```

* Указать количество (например, 5 фото):
```bash
python fetch_nasa_apod_images.py --count 5
```

* Комбинированно (папка `apod`, 5 фото):
```bash
python fetch_nasa_apod_images.py --folder apod --count 5
```

### `fetch_spacex_images.py` - скрипт для скачивания изображений запусков SpaceX.
Скрипт загружает фото запусков SpaceX в указанную папку.

* По умолчанию (последний запуск в images):
```bash
python fetch_spacex_images.py
```

* Выбрать папку (например, `spacex`):
```bash
python fetch_spacex_images.py --folder spacex
```

* Указать ID запуска (например, `5eb87d46ffd86e000604b388`):
```bash
python fetch_spacex_images.py --launch-id 5eb87d46ffd86e000604b388
```

* Комбинированно (папка `spacex`, конкретный запуск):
```bash
python fetch_spacex_images.py --folder spacex --launch-id 5eb87d46ffd86e000604b388
```


## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](dvmn.org).

## Лицензия

Проект лицензирован [MIT License](https://opensource.org/licenses/MIT). Полный текст лицензии доступен в файле `LICENSE`.
