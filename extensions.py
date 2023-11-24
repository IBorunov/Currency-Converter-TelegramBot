import json
import requests
from config import keys
class APIException (Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать сумму {amount}')

        if quote_ticker == base_ticker:
            raise APIException("вводите разные валюты!")

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        r = json.loads(r.content)
        total_base = r[base_ticker] * amount
        total_base = round(total_base, 4)
        return total_base


