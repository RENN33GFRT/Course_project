import logging
import re
from datetime import datetime, time, timedelta
from typing import Any, Dict, List, Union

from logging_config import setup_logging

setup_logging()
logger = logging.getLogger("my_log")


def greetings(actual_time: str) -> str:
    """
    Функция, принимающая время в виде строки в формате HH:MM:SS
    и возвращающая приветствие в зависимости от времени суток.
    """
    try:
        logger.info("Из переданной строки с датой создаем DataFrame")

        date_obj = datetime.strptime(actual_time, "%H:%M:%S")

        greets = ["Доброе утро!", "Добрый день!", "Добрый вечер!", "Доброй ночи!"]

        comparison_night = time(0, 0)
        comparison_morning = time(4, 0)
        comparison_day = time(12, 0)
        comparison_evening = time(17, 0)

        logger.info("Определяем какое приветствие подойдет для текущего времени суток")

        if comparison_night <= date_obj.time() < comparison_morning:
            return greets[3]
        elif comparison_morning <= date_obj.time() < comparison_day:
            return greets[0]
        elif comparison_day <= date_obj.time() < comparison_evening:
            return greets[1]
        else:
            return greets[2]

    except ValueError:
        logger.error("Передано неверное время")
        raise ValueError("Неверный формат времени")


def sort_by_date(operations_list: List[Dict[str, Any]], input_date: str) -> Union[str, List[Dict[str, Any]]]:
    """
    Функция, получающая список словарей с операциями и дату, возвращающая список, отфильтрованный
    по дате с начала месяца, на который выпадает входящая дата, по входящую дату.
    """
    pattern = re.compile(r"(\d{2})\.(\d{2})\.(\d{4})")

    result: List[Dict[str, Any]] = []

    logger.info("Проверяем переданную дату на корректный формат")

    if input_date and pattern.fullmatch(input_date):
        logger.info("Формат даты корректный")

        day_int = int(input_date[:2])
        input_date_obj = datetime.strptime(input_date, "%d.%m.%Y").date()

        start = input_date_obj - timedelta(days=(day_int - 1))
        stop = input_date_obj
        logger.info("Фильтруем операции по дате")

        for operation in operations_list:
            operation_date_obj = datetime.strptime(operation["Дата операции"], "%d.%m.%Y %H:%M:%S").date()
            if start <= operation_date_obj <= stop:
                result.append(operation)

    else:
        logger.warning("Введена неверная дата")
        print("Введена неверная дата. Введите дату в формате ДД.ММ.ГГГГ")

    return result


def get_card_info(operations_list: List[Dict[str, Any]]) -> List[Dict[str, Union[str, float]]]:
    """
    Функция, принимающая список операций и возвращающая список словарей с данными о картах:
    последние 4 цифры карты, общая сумма расходов, кешбэк (1 рубль на каждые 100 рублей) в формате
    [{"last_digits": "4 последние цифры номера карты",
      "total_spent": сумма расходов,
      "cashback": кэшбек},
    {...}]
    """
    card_data: Dict[str, float] = {}
    pattern = re.compile(r"\*\d{4}")

    logger.info("Определяем номер карты")
    for operation in operations_list:
        if isinstance(operation.get("Номер карты"), str) and pattern.fullmatch(operation["Номер карты"]):
            if "Сумма операции" in operation and "Статус" in operation:
                card_number = operation["Номер карты"][1:]
                amount = operation["Сумма операции"]

                logger.info("Проверяем статус каждой операции")

                if operation["Статус"] == "OK" and isinstance(amount, (int, float)) and amount < 0:
                    if card_number not in card_data:
                        logger.info("Считаем сумму операций по каждой карте")
                        card_data[card_number] = 0.0

                    card_data[card_number] += abs(float(amount))

    result: List[Dict[str, Union[str, float]]] = []
    logger.info("Формируем результат с данными о картах")

    for card_num, data in card_data.items():
        result.append({"last_digits": card_num, "total_spent": round(data, 2), "cashback": round(data * 0.01, 2)})

    return result


def get_top_transactions(operations_list: List[Dict[str, Any]]) -> List[Dict[str, Union[str, float]]]:
    """
    Функция, принимающая список словарей с операциями и возвращающая список из топ-5 транзакций по сумме
    в формате:
    [{"date": "дата",
      "amount": сумма,
      "category": "категория",
      "description": "описание"},
    {...}]
    """
    n = 5
    result: List[Dict[str, Union[str, float]]] = []

    negative_transactions = [
        operation
        for operation in operations_list
        if "Сумма операции" in operation
        and isinstance(operation["Сумма операции"], (int, float))
        and operation["Сумма операции"] < 0
    ]

    logger.info("Определяем топ-5 операций по сумме")

    top_5 = sorted(negative_transactions, key=lambda x: abs(x["Сумма операции"]), reverse=True)[:n]

    logger.info("Формируем данные для получения топ-5 операций в нужном формате")

    for el in top_5:
        date = el["Дата операции"].split()[0]
        amount = abs(el["Сумма операции"])
        category = el["Категория"]
        description = el["Описание"]

        result.append({"date": date, "amount": round(amount, 2), "category": category, "description": description})

    return result
