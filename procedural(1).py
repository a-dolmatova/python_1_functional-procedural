import requests
import json
import os


URL = 'https://api.forexrateapi.com/v1/latest?api_key=d1ec91b7fe280d12387b0b8314397dbf&base=USD&currencies=EUR,INR,JPY,AUD,BTC,KZT,RWF,RUB,TWD'
PATH = "data.json"

def get_data():
    '''Читает данные по URL и возвращает JSON.'''
    try:
        data = requests.get(URL, timeout = 10)
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

def load_last_data():
    '''Возвращает данные, записанные в path. Если такого файла нет - вернет None.'''
    if os.path.exists(PATH):
        with open(PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    return None

def find_falling_currency(last_data, new_data):
    '''Сравнивает курсы валют в старых и новых данных и выводит валюты, упавшие между запусками.'''
    for currency, value in new_data['rates'].items():
        if value < last_data['rates'][currency]:
            print(f"{currency} упала с {last_data['rates'][currency]} до {value}.")

def save_data(data):
    '''Записывает данные JSON в файл.'''
    with open(PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
    new_data = get_data()
    last_data = load_last_data()
    if new_data and last_data:
        find_falling_currency(last_data, new_data)  
    if new_data:
        save_data(new_data)

if __name__ == '__main__':
    main()