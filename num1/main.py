import logging
from pathlib import Path
from sources import fetch_from_api, load_last_from_db, save_to_db, init_db
from core_procedural import find_falling_currency_procedural
from core_functional import find_falling_currency_functional


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


if __name__ == '__main__':
    db_path = Path("python8/num1/exchange_rates.db")
    api_url = 'https://api.forexrateapi.com/v1/latest?api_key=d1ec91b7fe280d12387b0b8314397dbf&base=USD&currencies=EUR,INR,JPY,AUD,BTC,KZT,RWF,RUB,TWD'
    
    init_db(db_path)

    last_data = load_last_from_db(db_path)
    
    if not last_data:
        logging.warning("Не удалось загрузить старые данные.")
        new_data = fetch_from_api(api_url)
        if new_data:
            save_to_db(db_path, new_data)
            logging.info("Новые данные успешно получены и сохранены.")
        else:
            logging.error("Не удалось получить данные.")
            exit()
    else:
        new_data = fetch_from_api(api_url)
        if new_data:
            save_to_db(db_path, new_data)
            logging.info("Новые данные успешно получены и сохранены.")
            
            falling_currencies_procedural = find_falling_currency_procedural(last_data, new_data)
            falling_currencies_functional = find_falling_currency_functional(last_data, new_data)
            
            print(f"Валюты, которые упали (процедурный стиль): {falling_currencies_procedural}")
            print(f"Валюты, которые упали (функциональный стиль): {falling_currencies_functional}")
        else:
            logging.error("Не удалось получить данные с API.")
            exit()