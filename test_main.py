import pytest
import requests
from main import get_random_cat_image
from unittest.mock import patch, Mock


def test_successful_request():
    """
    Проверяет успешный запрос и возврат правильного URL
    """
    # Мокаем ответ API с валидными данными
    mock_response = Mock()
    mock_response.json.return_value = [
        {"url": "https://cdn2.thecatapi.com/images/abc.jpg"}
    ]
    mock_response.raise_for_status.return_value = None

    with patch('requests.get', return_value=mock_response) as mock_get:
        result = get_random_cat_image()
        mock_get.assert_called_once_with(
            "https://api.thecatapi.com/v1/images/search", timeout=5
        )
        assert result == "https://cdn2.thecatapi.com/images/abc.jpg"


def test_failed_request():
    """
    Проверяет обработку неуспешного запроса (404 ошибка)
    """
    # Мокаем исключение для 404 ошибки
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.HTTPError("404 Not Found")

        result = get_random_cat_image()
        assert result is None


def test_invalid_response_format():
    """
    Проверяет обработку невалидного формата ответа
    """
    # Мокаем ответ с неверным форматом данных
    mock_response = Mock()
    mock_response.json.return_value = {"error": "Invalid response"}
    mock_response.raise_for_status.return_value = None

    with patch('requests.get', return_value=mock_response):
        result = get_random_cat_image()
        assert result is None


def test_empty_response():
    """
    Проверяет обработку пустого ответа от API
    """
    # Мокаем пустой ответ
    mock_response = Mock()
    mock_response.json.return_value = []
    mock_response.raise_for_status.return_value = None

    with patch('requests.get', return_value=mock_response):
        result = get_random_cat_image()
        assert result is None