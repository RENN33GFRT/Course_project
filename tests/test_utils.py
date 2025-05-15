from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.utils import get_json_currencies, get_json_stocks, get_xlsx


@patch("pandas.read_excel")
def test_get_xlsx_success(mock_read_excel):
    """Тест успешного чтения XLSX файла"""
    test_df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    mock_read_excel.return_value = test_df

    result_dict, result_df = get_xlsx("test.xlsx")
    assert isinstance(result_dict, list)
    assert isinstance(result_df, pd.DataFrame)
    assert not result_df.empty


@patch("pandas.read_excel")
def test_get_xlsx_file_not_found(mock_read_excel):
    """Тест с отсутствующим файлом"""
    mock_read_excel.side_effect = FileNotFoundError
    result_dict, result_df = get_xlsx("nonexistent.xlsx")
    assert result_dict == []
    assert result_df.empty


def test_get_json_currencies_success():
    """Тест успешного чтения JSON с валютами"""
    test_data = '{"user_currencies": ["USD", "EUR"]}'
    with patch("builtins.open", mock_open(read_data=test_data)):
        result = get_json_currencies("test.json")
        assert result == ["USD", "EUR"]


def test_get_json_currencies_missing_key():
    """Тест JSON с отсутствующим ключом"""
    test_data = '{"wrong_key": []}'
    with patch("builtins.open", mock_open(read_data=test_data)):
        result = get_json_currencies("test.json")
        assert result == []


def test_get_json_stocks_success():
    """Тест успешного чтения JSON с акциями"""
    test_data = '{"user_stocks": ["AAPL", "GOOG"]}'
    with patch("builtins.open", mock_open(read_data=test_data)):
        result = get_json_stocks("test.json")
        assert result == ["AAPL", "GOOG"]
