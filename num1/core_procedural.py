from models import ExchangeRates


def find_falling_currency_procedural(last_data: ExchangeRates, new_data: ExchangeRates):
    '''Сравнивает курсы валют в старых и новых данных и выводит валюты, упавшие между запусками (процедурный стиль).'''
    falling_currencies = []
    for currency, new_value in new_data.get_all_rates().items():
        last_value = last_data.get_rate(currency)
        if new_value < last_value:
            falling_currencies.append(currency)
    return falling_currencies

def max_up_procedural(start: ExchangeRates, end: ExchangeRates):
    """Возвращает валюту и величину наибольшего роста курса (процедурный стиль)."""
    max_currency = ''
    max_change = float('-inf')
    for currency, start_val in start.get_all_rates().items():
        change = end.get_rate(currency) - start_val
        if change > max_change:
            max_change = change
            max_currency = currency
    return max_currency, max_change

def max_down_procedural(start: ExchangeRates, end: ExchangeRates):
    """Возвращает валюту и величину наибольшего падения курса (процедурный стиль)."""
    min_currency = ''
    min_change = float('inf')
    for currency, start_val in start.get_all_rates().items():
        change = end.get_rate(currency) - start_val
        if change < min_change:
            min_change = change
            min_currency = currency
    return min_currency, min_change

def stable_procedural(start: ExchangeRates, end: ExchangeRates):
    """Возвращает валюту и величину наименьшего изменения курса (процедурный стиль)."""
    stable_currency = ''
    stable_change = float('inf')
    for currency, start_val in start.get_all_rates().items():
        change = end.get_rate(currency) - start_val
        if abs(change) < stable_change:
            stable_change = change
            stable_currency = currency
    return stable_currency, stable_change