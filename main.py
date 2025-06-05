import requests


def get_random_cat_image():
    """
    Получает случайное изображение кошки с TheCatAPI
    Возвращает URL изображения при успешном запросе или None при ошибке
    """
    url = "https://api.thecatapi.com/v1/images/search"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Генерирует исключение для кодов 4xx/5xx

        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            return data[0].get('url')
        return None
    except (requests.RequestException, ValueError):
        return None