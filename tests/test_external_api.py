import json
from unittest.mock import patch

import pytest

from src.external_api import get_currency_rate, get_stock_price


@patch("requests.get")
def test_get_currency_rate(mock_get, result_of_currency_rate):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = json.loads(result_of_currency_rate)
    result = get_currency_rate("USD")
    assert result == {"currency": "USD", "rate": 111.66}


@patch("requests.get")
def test_get_currency_rate_error_code(mock_get):
    mock_get.return_value.status_code = 500

    with pytest.raises(Exception) as exc_info:
        get_currency_rate("USD")
    assert "Запрос не был успешным." in str(exc_info.value)


@patch("requests.get")
def test_get_currency_rate_without_result(mock_get, result_of_currency_rate_without_result):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = json.loads(result_of_currency_rate_without_result)

    with pytest.raises(ValueError) as exc_info:
        get_currency_rate("USD")

    assert str(exc_info.value) == "Недостаточно данных"


@patch("requests.get")
def test_get_stock_price(mock_get, result_of_stocks):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = json.loads(result_of_stocks)
    result = get_stock_price("AAPL")

    assert result == {"stock": "AAPL", "price": 75.09}


@patch("requests.get")
def test_get_stock_price_failed(mock_get, result_of_stocks_failed):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = json.loads(result_of_stocks_failed)

    with pytest.raises(Exception) as exc_info:
        get_stock_price("GOOGL")

    assert str(exc_info.value) == "Нет данных о цене для данной акции."


@patch("requests.get")
def test_get_stock_price_with_error(mock_get):
    mock_get.return_value.status_code = 500

    with pytest.raises(Exception) as exc_info:
        get_stock_price("AAPL")

    assert "Запрос не был успешным. Возможная причина:" in str(exc_info)
