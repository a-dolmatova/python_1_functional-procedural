import requests
import time


URL = 'https://api.forexrateapi.com/v1/latest?api_key=d1ec91b7fe280d12387b0b8314397dbf&base=USD&currencies=EUR,INR,JPY,AUD,BTC,KZT,RWF,RUB,TWD'
TIME = 60
# TIME = 3600

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

def analyze_data(start_data, end_data):
    '''Анализирует начальные и конечные курсы валют и выводит валюту, которая больше всего 
    взлетела, валюту, которая больше всего упала, и самую стабильную валюту.'''
    max_up_value = 0
    max_up_currency = ''
    
    max_down_value = 0
    max_down_currency = ''
    
    stable_value = 100
    stable_currency = ''

    for currency, value in start_data['rates'].items():
        change = end_data['rates'][currency] - start_data['rates'][currency]

        if change > max_up_value:
            max_up_value = change
            max_up_currency = currency
            
        if change < max_down_value:
            max_down_value = change
            max_down_currency = currency
            
        if abs(change) < stable_value:
            stable_value = change
            stable_currency = currency

    print(f"Больше всего взлетела валюта {max_up_currency}: на {max_up_value}.")  if max_up_currency else print("Никакая валюта не взлетела.")
    print(f"Больше всего упала валюта {max_down_currency}: на {max_down_value}.") if max_down_currency else print("Никакая валюта не упала.")
    print(f"Самая стабильная валюта - {stable_currency} с изменением {stable_value}.")
    
def main():
    start_data = get_data()
    time.sleep(TIME)
    end_data = get_data()
    if start_data and end_data:
        analyze_data(start_data, end_data)
    
if __name__ == '__main__':
    main()