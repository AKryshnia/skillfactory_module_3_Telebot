import requests
import json
from config import keys


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            if base and quote == 'рубль':
                raise APIException(f'Невозможна конвертация рублей в рубли.')
            elif base and quote == 'евро':
                raise APIException(f'Невозможна конвертация евро в евро.')
            elif base and quote == 'доллар':
                raise APIException(f'Невозможна конвертация долларов в доллары.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {quote}. Введите правильное значение.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {base}. Введите правильное значение.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество: {amount}. Введите правильное значение.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        total_base = round(total_base * amount, 3)  # Округляем получившееся значение, чтобы не было некрасивых длинных чисел

        return total_base
