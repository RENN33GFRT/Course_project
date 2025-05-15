import json

import pytest

from src.services import get_profitable_cashback_categories


def test_get_profitable_cashback_categories_success():
    """Тест успешного получения категорий кешбэка"""
    test_data = [
        {"Дата операции": "01.01.2023 12:00:00", "Категория": "Food", "Сумма операции": -1000},
        {"Дата операции": "15.01.2023 12:00:00", "Категория": "Transport", "Сумма операции": -500},
    ]

    result = get_profitable_cashback_categories(test_data, "2023", "01")
    result_dict = json.loads(result)
    assert "Food" in result_dict
    assert result_dict["Food"] == 10.0
    assert result_dict["Transport"] == 5.0


def test_get_profitable_cashback_categories_invalid_data():
    """Тест с некорректными входными данными"""
    result = get_profitable_cashback_categories("not a list", "2023", "01")
    assert result == "{}"


def test_get_profitable_cashback_categories_empty_data():
    """Тест с пустыми данными"""
    result = get_profitable_cashback_categories([], "2023", "01")
    assert result == "{}"
