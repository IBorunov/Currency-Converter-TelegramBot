import telebot
from config import TOKEN
from extensions import APIException, Converter


bot = telebot.TeleBot(TOKEN)




@bot.message_handler(commands=['start', 'help'])
def start_and_help(message: telebot.types.Message):
    text = ('Привет! Этот бот показывает цену на определённое количество валюты!\n'
            'Просто укажите <Название конвертируемой валюты>, <в какую валюту перевести>, <Сумму конвертации>.\n'
            'Вводите значения без запятых!\n'
            'Чтобы увидеть список всех валют, введите команду /values')
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values_command(message: telebot.types.Message):
    text = 'Доступные валюты: Рубль, Доллар, Евро'
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise APIException("вводите ровно 3 значения, без запятых!")

        quote, base, amount = values
        total_base = Converter.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message,f'Ошибка пользователя: \n {e}')

    except Exception as e:
        bot.reply_to(message, f'Серверная ошибка: \n {e}')
    else:
        text = f'Цена за {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)

