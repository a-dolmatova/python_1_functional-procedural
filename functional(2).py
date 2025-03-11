import requests
import json
import os

URL = 'https://api.forexrateapi.com/v1/latest?api_key=d1ec91b7fe280d12387b0b8314397dbf&base=USD&currencies=EUR,INR,JPY,AUD,BTC,KZT,RWF,RUB,TWD'
PATH = "data.json"

def get_data(url):
    '''Читает данные по URL и возвращает JSON. Если произошла ошибка - вернет None.'''
    try:
        data = requests.get(url, timeout = 10)
        data.raise_for_status()
        return data.json()
    except requests.exceptions.ConnectionError:
        print("Ошибка: нет подключения к интернету или сервер недоступен.")
    except requests.exceptions.Timeout:
        print("Ошибка: превышено время ожидания ответа от сервера.")
    except requests.exceptions.HTTPError as error:
        print(f"Ошибка HTTP: {error}")
    except requests.exceptions.JSONDecodeError:
        print("Ошибка: невалидный JSON.")
    return None

def load_data(path):
    '''Возвращает данные, записанные в path. Если такого файла нет - вернет None.'''
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    return None

def find_falling_currency(new_data, last_data):
    '''Сравнивает курсы валют в старых и новых данных и возвращает валюты, упавшие между запусками.'''
    return list(filter(lambda currency: new_data['rates'][currency] < last_data['rates'][currency], new_data['rates']))

def save_data(data, path):
    '''Записывает данные JSON в файл path.'''
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    
if __name__ == '__main__':
    new_data = get_data(URL)
    last_data = load_data(PATH)
    if new_data and last_data:
        print("\n".join(map(lambda currency: f"{currency} упала с {last_data['rates'][currency]} до {new_data['rates'][currency]}.", 
                            find_falling_currency(new_data, last_data))))
    if new_data:
        save_data(new_data, PATH)