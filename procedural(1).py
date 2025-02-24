import requests
import json
import os


URL = 'https://api.forexrateapi.com/v1/latest?api_key=d1ec91b7fe280d12387b0b8314397dbf&base=USD&currencies=EUR,INR,JPY,AUD,BTC,KZT,RWF,RUB,TWD'


if __name__ == '__main__':
    
    # Чтение данных по URL.
    data = requests.get(URL)
    new_data = data.json()
    
    # Чтение данных, записанных в предыдущих запусках скрипта, если это не первый запуск.
    if os.path.exists("data.json"):
        with open("data.json", "r", encoding="utf-8") as file:
            last_data = json.load(file)
                    
            # Сравнение стоимостей валют в в старых и новых данных и вывод валют, упавших между запусками.
            for currency, value in new_data['rates'].items():
                if value < last_data['rates'][currency]:
                    print(f"{currency} упала с {last_data['rates'][currency]} до {value}.")
                    
    # Запись новых данных в файл.
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(new_data, file, indent=4, ensure_ascii=False)