import requests
import json
from config import keys


class Bot_Exception(Exception):
    pass


class Bot_Convector:
    @staticmethod
    def convert(currency: str, base: str, value: str):

        if currency == base:
            raise Bot_Exception('Считать нужно разные валюты, введены одинаковые')

        try:
            keys[currency]
        except KeyError:
            raise Bot_Exception(
                f'Ошибка ввода первой валюты, проверьте доступные валюты в /values\nВы ввели <{currency}>')
        try:
            keys[base]
        except KeyError:
            raise Bot_Exception(f'Ошибка ввода второй валюты, проверьте доступные валюты в /values \nВы ввели <{base}>')
        try:
            if ',' in value:
                value = value.replace(',', '') #также решил, обрабатывать копейки(центы и т.д.), и чтобы не ловить ошибку на запятой,
                # и не заставлять пользователя исправлять на точку, избавляюсь от нее сам для удобства пользователя.

            float(value)
        except:
            raise Bot_Exception(
                f'Ошибка ввода количества валюты, нужно вводить число,\nЕсли число нецелое, то через запятую или точку\n'
                f'Было введено <{value}>')

        new_request = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={keys.get(currency)}&tsyms={keys.get(base)}')
        total_base = json.loads(new_request.content)[keys.get(base)]
        return total_base
