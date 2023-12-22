import telebot
import re
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message):
    bot.send_message(message.chat.id, f"Добро пожаловать в маленький бот конвертации валют, {message.chat.username}!\nЧтобы начать работу, введите команду боту в следующем формате:\n<имя валюты, цену которой Вы хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты>\
 <количество переводимой валюты> (через пробел)\nУвидеть список всех доступных валют можно по команде: /values")


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Указаны неверные параметры. Введите правильные значения!')

        quote, base, amount = values
        quote = quote.lower()
        base = base.lower()
        amount = float(re.sub(",", ".", amount))
        total_base = CurrencyConverter.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:  # Делаем корректировку в связи с грамматикой русского языка :) Получилось громоздко, к сожалению, пока учусь дружить с pymorphy
        if quote == 'рубль' and base == 'доллар':
            text = f'Стоимость {amount} рублей в долларах - {total_base}'
        elif quote == 'доллар' and base == 'рубль':
            text = f'Стоимость {amount} долларов в рублях - {total_base}'
        elif quote == 'рубль' and base == 'евро':
            text = f'Стоимость {amount} рублей в евро - {total_base}'
        elif quote == 'евро' and base == 'рубль':
            text = f'Стоимость {amount} евро в рублях - {total_base}'
        elif quote == 'евро' and base == 'доллар':
            text = f'Стоимость {amount} евро в долларах - {total_base}'
        elif quote == 'доллар' and base == 'евро':
            text = f'Стоимость {amount} долларов в евро - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
