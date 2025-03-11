import requests
import time


URL = 'https://api.forexrateapi.com/v1/latest?api_key=d1ec91b7fe280d12387b0b8314397dbf&base=USD&currencies=EUR,INR,JPY,AUD,BTC,KZT,RWF,RUB,TWD'

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

def max_up(start_data, end_data):
    '''Анализирует начальные и конечные курсы валют и выводит валюту, которая больше всего взлетела.'''
    return max(dict(map(lambda currency : (currency, end_data['rates'][currency] - start_data['rates'][currency]), start_data['rates'])).items(), key = lambda x: x[1])

def max_down(start_data, end_data):
    '''Анализирует начальные и конечные курсы валют и выводит валюту, которая больше всего упала.'''
    return min(dict(map(lambda currency : (currency, end_data['rates'][currency] - start_data['rates'][currency]), start_data['rates'])).items(), key = lambda x: x[1])

def stable(start_data, end_data):
    '''Анализирует начальные и конечные курсы валют и выводит самую стабильную валюту.'''
    return min(dict(map(lambda currency : (currency, end_data['rates'][currency] - start_data['rates'][currency]), start_data['rates'])).items(), key = lambda x: abs(x[1]))

if __name__ == '__main__':
    start_data = get_data(URL)
    time.sleep(60)
    end_data = get_data(URL)
    
    if end_data and start_data:
        print(f"Валюта с самым большим ростом: {max_up(start_data, end_data)}.")
        print(f"Валюта с самым большим ростом: {max_down(start_data, end_data)}.")
        print(f"Самая стабильная валюта: {stable(start_data, end_data)}.")