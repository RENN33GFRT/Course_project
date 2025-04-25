import logging
import os
from datetime import datetime, timedelta
from typing import Dict, Union

import requests
from dotenv import load_dotenv

from logging_config import setup_logging

setup_logging()
logger = logging.getLogger("my_log")

load_dotenv()
CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")
STOCK_API_KEY = os.getenv("STOCK_API_KEY")


def get_currency_rate(currency: str, amount: int = 1) -> Dict[str, Union[str, float]]:
    """
    Функция, принимающая на вход валюту для конвертации, сумму (по умолчанию 1) и возвращающая словарь в формате:
    {"currency": "валюта",
     "rate": стоимость в рублях}
    """
    logger.info("Определяем url и др. необходимые объекты")

    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"
    headers = {"apikey": CURRENCY_API_KEY}
    response = requests.get(url, headers=headers)
    status_code = response.status_code

    logger.info("Проверяем статус код")

    if status_code == 200:

        logger.info("Статус код 200. Запрос выполнен успешно.")
        logger.info("Преобразование ответа в формат JSON")

        content = response.json()

        logger.info("Проверка на наличие необходимого ключа в ответе")

        if content["result"]:

            logger.info("Необходимый ключ найден")
            logger.info("Получение результата и запись в словарь")

            result = {"currency": currency, "rate": round(content["result"], 2)}

            return result

        else:

            logger.error("Необходимый ключ не найден")

            raise ValueError("Недостаточно данных")

    else:

        logger.error(f"Статус код не равен 200. Возможная ошибка: {response.reason}")

        raise Exception(f"Запрос не был успешным. Возможная причина: {response.reason}")


def get_stock_price(stock: str) -> Dict[str, Union[str, float]]:
    """
    Функция, принимающая название акции и возвращающая словарь в формате:
    {"stock": "Название акции",
      "price": стоимость акции}
    """
    logger.info("Определяем url и др. необходимые объекты")

    date_yesterday = datetime.now() - timedelta(days=1)
    three_days_ago = datetime.now() - timedelta(days=3)
    stop_date = date_yesterday.strftime("%Y-%m-%d")
    start_date = three_days_ago.strftime("%Y-%m-%d")
    headers = {"apikey": STOCK_API_KEY}
    url = f"https://api.polygon.io/v2/aggs/ticker/{stock}/range/1/day/{start_date}/{stop_date}?apiKey={STOCK_API_KEY}"

    response = requests.get(url, headers=headers)

    status_code = response.status_code

    logger.info("Проверяем статус код")

    if status_code == 200:

        logger.info("Статус код 200. Запрос выполнен успешно.")
        logger.info("Преобразование ответа в формат JSON")

        content = response.json()

        logger.info("Проверка на наличие необходимого ключа в ответе")

        if content["status"] == "OK" and content["results"][0]["c"]:

            logger.info("Необходимый ключ найден")
            logger.info("Получение результата и запись в словарь")

            result = {"stock": stock, "price": round(content["results"][0]["c"], 2)}

            return result

        else:

            logger.error("Необходимый ключ не найден")

            raise Exception("Нет данных о цене для данной акции.")

    else:

        logger.error(f"Статус код не равен 200. Возможная ошибка: {response.reason}")

        raise Exception(f"Запрос не был успешным. Возможная причина: {response.reason}")
