from datetime import datetime, timedelta

import pytest

from src.views import get_card_info, get_top_transactions, greetings, sort_by_date


def test_greetings_morning():
    """Тест приветствия для утра"""
    assert greetings("08:00:00") == "Доброе утро!"


def test_greetings_afternoon():
    """Тест приветствия для дня"""
    assert greetings("13:00:00") == "Добрый день!"


def test_greetings_evening():
    """Тест приветствия для вечера"""
    assert greetings("18:00:00") == "Добрый вечер!"


def test_greetings_night():
    """Тест приветствия для ночи"""
    assert greetings("02:00:00") == "Доброй ночи!"


def test_greetings_invalid_time():
    """Тест с некорректным временем"""
    with pytest.raises(ValueError):
        greetings("invalid_time")


def test_sort_by_date_success():
    """Тест успешной сортировки по дате"""
    test_data = [
        {"Дата операции": "01.01.2023 12:00:00"},
        {"Дата операции": "15.01.2023 12:00:00"},
        {"Дата операции": "01.02.2023 12:00:00"},
    ]
    result = sort_by_date(test_data, "15.01.2023")
    assert len(result) == 2


def test_sort_by_date_invalid_date():
    """Тест с некорректной датой"""
    result = sort_by_date([], "invalid_date")
    assert result == []


def test_get_card_info_success():
    """Тест успешного получения информации о картах"""
    test_data = [
        {"Номер карты": "*1234", "Сумма операции": -100, "Статус": "OK"},
        {"Номер карты": "*1234", "Сумма операции": -200, "Статус": "OK"},
    ]
    result = get_card_info(test_data)
    assert len(result) == 1
    assert result[0]["last_digits"] == "1234"
    assert result[0]["total_spent"] == 300
    assert result[0]["cashback"] == 3.0


def test_get_top_transactions():
    """Тест получения топ-5 транзакций"""
    test_data = [
        {"Дата операции": "01.01.2023 12:00:00", "Сумма операции": -100, "Категория": "A", "Описание": "Desc1"},
        {"Дата операции": "02.01.2023 12:00:00", "Сумма операции": -500, "Категория": "B", "Описание": "Desc2"},
        {"Дата операции": "03.01.2023 12:00:00", "Сумма операции": -200, "Категория": "C", "Описание": "Desc3"},
    ]
    result = get_top_transactions(test_data)
    assert len(result) == 3
    assert result[0]["amount"] == 500
