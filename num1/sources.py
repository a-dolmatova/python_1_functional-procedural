import logging
import sqlite3
from pathlib import Path
import requests
import datetime
from models import ExchangeRates


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def init_db(db_path: Path):
    """Создаёт базу данных и таблицу, если их ещё нет."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS exchange_rates (
                base TEXT,
                currency TEXT,
                rate REAL,
                date TEXT
            )
        """)

def save_to_db(db_path: Path, rates: ExchangeRates):
    """Сохраняет данные в базу данных."""
    today = datetime.date.today().isoformat()
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        for currency, rate in rates.rates.items():
            cursor.execute("""
                INSERT INTO exchange_rates (base, currency, rate, date)
                VALUES (?, ?, ?, ?)
            """, (rates.base, currency, rate, today))
        conn.commit()
    logging.info("Данные успешно сохранены в базу данных.")

def load_last_from_db(db_path: Path):
    """Загружает актуальные курсы валют из БД."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT base, currency, rate
            FROM exchange_rates
            WHERE date = (SELECT MAX(date) FROM exchange_rates)
        """)
        rows = cursor.fetchall()
        if not rows:
            logging.warning("База данных пуста.")
            return None
        base = rows[0][0]
        rates = {currency: rate for _, currency, rate in rows}
        return ExchangeRates(base=base, rates=rates)

def fetch_from_api(url: str):
    """Получает данные с API и возвращает объект ExchangeRates."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        logging.info("Данные успешно получены с API.")
        return ExchangeRates(base=data['base'], rates=data['rates'])
    except requests.exceptions.ConnectionError:
        logging.error("Ошибка: нет подключения к интернету или сервер недоступен.")
    except requests.exceptions.Timeout:
        logging.error("Ошибка: превышено время ожидания ответа от сервера.")
    except requests.exceptions.HTTPError as error:
        logging.error(f"Ошибка HTTP: {error}")
    except requests.exceptions.JSONDecodeError:
        logging.error("Ошибка: невалидный JSON.")
    return None