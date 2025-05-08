from dataclasses import dataclass
from typing import Dict


@dataclass
class ExchangeRates:
    base: str
    rates: Dict[str, float]
    
    def get_all_rates(self):
        """Получение словаря с курсами валют."""
        return self.rates
    
    def get_rate(self, currency: str):
        """Получение курса необходимой валюты."""
        if currency not in self.rates:
            raise ValueError(f"Курс валюты {currency} не найден")
        return self.rates.get(currency)