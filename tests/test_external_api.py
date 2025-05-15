from unittest.mock import MagicMock, patch

import pytest

from src.external_api import get_currency_rate, get_stock_price


@patch("requests.get")
def test_get_currency_rate_success(mock_get):
    """Тест успешного получения курса валюты"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 75.5}
    mock_get.return_value = mock_response

    with patch.dict("os.environ", {"CURRENCY_API_KEY": "test_key"}):
        result = get_currency_rate("USD")
        assert result == {"currency": "USD", "rate": 75.5}


@patch("requests.get")
def test_get_currency_rate_failure(mock_get):
    """Тест неудачного запроса курса валюты"""
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.reason = "Bad Request"
    mock_get.return_value = mock_response

    with patch.dict("os.environ", {"CURRENCY_API_KEY": "test_key"}):
        with pytest.raises(Exception):
            get_currency_rate("USD")


@patch("requests.get")
def test_get_stock_price_success(mock_get):
    """Тест успешного получения цены акции"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "OK", "results": [{"c": 150.75}]}
    mock_get.return_value = mock_response

    with patch.dict("os.environ", {"STOCK_API_KEY": "test_key"}):
        result = get_stock_price("AAPL")
        assert result == {"stock": "AAPL", "price": 150.75}


@patch("requests.get")
def test_get_stock_price_failure(mock_get):
    """Тест неудачного запроса цены акции"""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.reason = "Not Found"
    mock_get.return_value = mock_response

    with patch.dict("os.environ", {"STOCK_API_KEY": "test_key"}):
        with pytest.raises(Exception):
            get_stock_price("AAPL")
