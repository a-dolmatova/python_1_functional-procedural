import requests
import time


if __name__ == '__main__':
    # Чтение данных по URL. Далее останавливаем программу на нужное количество секунд и снова считываем данные.
    start_data = requests.get('https://api.forexrateapi.com/v1/latest?api_key=d1ec91b7fe280d12387b0b8314397dbf&base=USD&currencies=EUR,INR,JPY,AUD,BTC,KZT,RWF,RUB,TWD').json()
    time.sleep(60)
    end_data = requests.get('https://api.forexrateapi.com/v1/latest?api_key=d1ec91b7fe280d12387b0b8314397dbf&base=USD&currencies=EUR,INR,JPY,AUD,BTC,KZT,RWF,RUB,TWD').json()
    
    # Создаём словарь с изменениями курса валют, используя map. Находим статистику, используя функции min() и max().  
    changes = dict(map(lambda currency : (currency, end_data['rates'][currency] - start_data['rates'][currency]), start_data['rates']))
    max_up_currency, max_up_value = max(changes.items(), key = lambda x: x[1])
    max_down_currency, max_down_value = min(changes.items(), key = lambda x: x[1])
    stable_currency, stable_value = min(changes.items(), key = lambda x: abs(x[1]))

    print(f"Больше всего взлетела валюта {max_up_currency}: на {max_up_value}.")  if any(change > 0 for change in changes.values()) else print("Никакая валюта не взлетела.")
    print(f"Больше всего упала валюта {max_down_currency}: на {max_down_value}.") if any(change < 0 for change in changes.values()) else print("Никакая валюта не упала.")
    print(f"Самая стабильная валюта - {stable_currency} с изменением {stable_value}.")