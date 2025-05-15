from datetime import datetime, timedelta

import pandas as pd
import pytest

from src.reports import spending_by_category


def test_spending_by_category_success():
    """Тест успешного формирования отчета по категории"""
    test_data = {
        "Дата платежа": ["01.01.2023", "15.01.2023", "01.02.2023"],
        "Категория": ["Food", "Food", "Transport"],
        "Сумма операции": [-100, -200, -50],
    }
    df = pd.DataFrame(test_data)

    result = spending_by_category(df, "Food", "15.02.2023")
    assert not result.empty
    assert result.iloc[0]["Категория"] == "Food"
    assert result.iloc[0]["Сумма трат"] == 300


def test_spending_by_category_missing_columns():
    """Тест с отсутствующими колонками в данных"""
    test_data = {"WrongColumn": [1, 2, 3]}
    df = pd.DataFrame(test_data)

    result = spending_by_category(df, "Food")
    assert result.empty


def test_spending_by_category_invalid_date():
    """Тест с некорректной датой"""
    test_data = {"Дата платежа": ["01.01.2023"], "Категория": ["Food"], "Сумма операции": [-100]}
    df = pd.DataFrame(test_data)

    with pytest.raises(ValueError):
        spending_by_category(df, "Food", "invalid_date")
