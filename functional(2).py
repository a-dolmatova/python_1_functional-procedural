import requests
import json
import os


if __name__ == '__main__':

    # Чтение данных по URL.
    new_data = requests.get('https://api.forexrateapi.com/v1/latest?api_key=d1ec91b7fe280d12387b0b8314397dbf&base=USD&currencies=EUR,INR,JPY,AUD,BTC,KZT,RWF,RUB,TWD').json()

    # Чтение данных, записанных в предыдущих запусках скрипта, если это первый запуск - считаем предыдущие данные новыми и код ничего не выведет, как и должен. 
    last_data = json.load(open("data.json", "r", encoding="utf-8")) if os.path.exists("data.json") else new_data
    
    # Используя filter(), находим упавшие между запусками валюты.
    falling_currencies = list(filter(lambda currency: new_data['rates'][currency] < last_data['rates'][currency], new_data['rates']))

    # Используя map(), формируем текстовые строки вывода.
    print("\n".join(map(lambda currency: f"{currency} упала с {last_data['rates'][currency]} до {new_data['rates'][currency]}.", falling_currencies)))
    
    # Записываем новые данные в файл.
    json.dump(new_data, open("data.json", "w", encoding="utf-8"), indent=4, ensure_ascii=False)