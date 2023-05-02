#!/usr/bin/python3

from extensions import *
import telebot
from tele_token import API_TOKEN, VALUTE_API_SITE


def tele():

    bot = telebot.TeleBot(API_TOKEN)
    c = Conversion(VALUTE_API_SITE)

    # Обработка команды '/start' и '/help'
    @bot.message_handler(commands=['help', 'start'])
    def send_welcome(message):
        bot.reply_to(message, """\
       Привет! Я бот, помогу сделать конвертацию из одной валюты в другую, или узнать стоимость в рублях.\n\
    Чтобы узнать список доступных валют, введите команду /values.\n\
    Чтобы узнать стоимость валюты в рублях, введите 1.количество 2.название валюты.\n\
    Чтобы сконвертировать одну валюту в другую, введите 1. количество 2. что конвертируете 3.в какую валюту.\n\
    Все значения нужно вводить через пробел или с новой строки.\n\
    Приятной работы!
    """)

    # Обработка команды '/values'
    @bot.message_handler(commands=['values'])
    def send_welcome(message):
        bot.reply_to(message, c.request())

    # Обработка остальных сообщений с content_type = 'text' (по-умолчанию)
    @bot.message_handler(content_types=['text'])
    def get_acq(message: telebot.types.Message):
        words = message.text.split()
        if len(words) == 3:
            amount, quote, base = words
            try:
                val = f"Стоимость {amount} {quote} составляет {c.get_price(quote, base, amount):0.3f} {base}"
            except Exception as e:
                val = e
        elif len(words) == 2:
            amount, quote = words
            try:
                val = f"Стоимость {amount} {quote} составляет {c.get_price(quote, '', amount):0.3f} RUB"
            except Exception as e:
                val = e
        else:
            val = "Некорректный запрос. Введите 1.количество, 2.название валюты, 3.в какой валюте расчет(опц.)"
        bot.reply_to(message, val)

    # запуск бота в бесконечном цикле ожидания
    bot.infinity_polling()


if __name__ == '__main__':
    # ****************************** #
    # Телеграм-бот @UNIAPBHELPER_BOT #
    # ****************************** #

    tele()
