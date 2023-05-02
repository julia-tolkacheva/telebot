import requests
import json


# определение пользовательских исключений
class Error(Exception):
    """Базовый класс для других исключений"""
    pass


class ConvertException(Error):
    """Исключение при неправильном запросе конвертации"""
    pass


class Conversion:

    def __init__(self, site):
        r = requests.get(site)
        texts = json.loads(r.content)
        self.valutes = texts['Valute']
        self.timestamp = texts['Timestamp']

    def one_coin_price(self, coin_name):
        return self.valutes[coin_name]['Value'] / self.valutes[coin_name]['Nominal']

    def get_price(self, quote, base, amount):
        ticks = [key for key in self.valutes]
        if quote not in ticks:
            raise ConvertException(f"заданная Вами валюта {quote} не содержится в списке доступных валют")

        if base and base not in ticks:
            raise ConvertException(f"заданная Вами валюта {base} не содержится в списке доступных валют")
        try:
            amount = int(amount)
        except ValueError:
            raise ConvertException(f"заданное значение {amount} не является числом")

        if base:
            return (self.one_coin_price(quote) / self.one_coin_price(base)) * amount
        else:
            return self.one_coin_price(quote) * amount

    def request(self):
        values = f"Данные с сайта www.cbr-xml-daily.ru\n" \
                 f"актуализированны {self.timestamp}\n" \
                 f"***********************************\n"
        for k in self.valutes:
            val = self.valutes[k]
            print(k, val)
            values += f"{val['CharCode']} : {val['Nominal']} {val['Name']} = {val['Value']} рублей\n"

        return values
