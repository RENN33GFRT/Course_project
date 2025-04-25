import json
import logging

import pandas as pd

from logging_config import setup_logging

setup_logging()
logger = logging.getLogger("my_log")


def get_xlsx(file_path: str) -> tuple[list[dict], pd.DataFrame]:
    """
    Функция, принимающая путь до Excel-файла и возвращающая список словарей и DataFrame.
    """
    try:
        logger.info("Чтение данных из Excel-файла")

        df = pd.read_excel(file_path)

        logger.info("Проверка данных из файла на корректность")

        if isinstance(df, pd.DataFrame) and not df.empty:
            logger.info("Данные корректны. Конвертация в словарь и возврат DataFrame")
            return df.to_dict(orient="records"), df
        else:
            logger.warning("Данные в файле отсутствуют или не являются DataFrame")
            return [], pd.DataFrame()

    except FileNotFoundError:
        logger.warning("Файл по переданному пути отсутствует")
        return [], pd.DataFrame()


def get_json_currencies(file_path: str) -> list:
    """
    Функция, принимающая путь к JSON файлу и возвращающая список данных из файла.
    """
    result = []

    try:
        logger.info("Попытка открыть JSON файл")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            logger.info("Файл открыт успешно")
            logger.info("Проверка на наличие нужного ключа")

            if "user_currencies" in data:
                logger.info("Ключ найден.")
                logger.info("Список необходимых данных получен")

                result = data["user_currencies"]

            else:
                logger.error("Ключ не найден")

        return result

    except json.JSONDecodeError as ex:
        logger.error(f"Невозможно декодировать JSON данные из файла. Возможная причина: {ex}")

        raise ValueError(f"Ошибка при чтении файла: {ex}")

    except Exception as ex:
        logger.error(f"Невозможно получить необходимые данные Возможная ошибка: {ex}")

        raise Exception(f"Ошибка при чтении файла: {ex}")


def get_json_stocks(file_path: str) -> list:
    """
    Функция, принимающая путь к JSON файлу и возвращающая список данных из файла.
    """
    result = []

    try:

        logger.info("Попытка открыть JSON файл")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            logger.info("Файл открыт успешно")
            logger.info("Проверка на наличие нужного ключа")

            if "user_stocks" in data:
                result = data["user_stocks"]

                logger.info("Ключ найден.")
                logger.info("Список необходимых данных получен")

            else:
                logger.error("Ключ не найден")

            return result

    except json.JSONDecodeError as ex:
        logger.error(f"Невозможно декодировать JSON данные из файла. Возможная причина: {ex}")

        raise ValueError(f"Ошибка при чтении файла: {ex}")

    except Exception as ex:
        logger.error(f"Невозможно получить необходимые данные Возможная ошибка: {ex}")

        raise Exception(f"Ошибка при чтении файла: {ex}")
