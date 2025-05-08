from models import ExchangeRates
from operator import itemgetter


def get_changes(start: ExchangeRates, end: ExchangeRates):
    """Возвращает итератор пар (валюта, изменение курса)."""
    return map(lambda cur: (cur, end.get_rate(cur) - start.get_rate(cur)), start.get_all_rates())

def find_falling_currency_functional(last_data: ExchangeRates, new_data: ExchangeRates):
    '''Сравнивает курсы валют в старых и новых данных и возвращает валюты, упавшие между запусками (функциональный стиль).'''
    return list(map(itemgetter(0), filter(lambda pair: pair[1] < 0, get_changes(last_data, new_data))))

def pick_change(fn, key):
    """Возвращает функцию, выбирающую экстремум (max или min) изменений курса по ключу key."""
    return lambda start, end: fn(get_changes(start, end), key=key)

max_up_functional = pick_change(max, key=lambda p: p[1])
max_up_functional.__doc__ = "Возвращает валюту и величину наибольшего роста курса (функциональный стиль)."

max_down_functional = pick_change(min, key=lambda p: p[1])
max_down_functional.__doc__ = "Возвращает валюту и величину наибольшего падения курса (функциональный стиль)."

stable_functional = pick_change(min, key=lambda p: abs(p[1]))
stable_functional.__doc__ = "Возвращает валюту и величину наименьшего изменения курса (функциональный стиль)."