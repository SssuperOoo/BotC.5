import telebot
from config import keys, TOKEN
from extensions import Bot_Convector, Bot_Exception

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    if message.text == '/help':  # Решил добавить небольшое отличие между командами старт и хэлп, в одном приветствие и инструкция,
        # во втором сообщение о готовности помочь и инструкция
        bot.reply_to(message,
                     f"Сейчас помогу, {message.chat.username}\nДанный бот создан для того, чтобы предоставить доступ"
                     f"к конвертации самых популярных валют\nФормат ввода: \n<Имя валюты> <В какую валюту переводит> <Количество переводимой валюты>"
                     f"\nНапример: рубль доллар 200\nЧтобы увидеть список доступной валюты введи - /values")
    if message.text == '/start':
        bot.reply_to(message,
                     f"Приветствую тебя, {message.chat.username} \nДанный бот создан для того, чтобы предоставить доступ"
                     f"к конвертации самых популярных валют\nФормат ввода: \n<Имя валюты> <В какую валюту переводит> <Количество переводимой валюты>"
                     f"\nНапример: рубль доллар 200\nЧтобы увидеть список доступной валюты введи - /values")


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    key_list = [] #Добавляю ключи в словарь, т.к. мне удобней и понятней работать через словарь.
    for key in keys:
        key_list.append(key)
    bot_keys = '\n'.join(key_list)
    bot.reply_to(message, f"Доступные валюты: \n{bot_keys}")



@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        my_message = message.text.lower().split(' ') #Делаю бота регистронезависимым, ведь в Телеграме чаще сидят с телефона,
        # где по умолчанию сообщения начинаются с большой буквы, и чтобы не было вызова наших исключений и не докучать пользователю,
        # просто обработаем его запрос в любом регистре.
        if len(my_message) != 3:
            raise Bot_Exception('Не правильное количество параметров\n'
                                'Ввод должен быть таким:\n<валюта1> <валюта2> <число>\nПример ввода: доллар рубль 1000\nПроверьте доступные валюты в /values')
        currency, base, value = my_message
        total_base = Bot_Convector.convert(currency, base, value) #получаем наш курс и обрабатываем ошибки
    except Bot_Exception as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось отработать команду\n{e}')

    else:
        text = f'{value} {keys.get(currency)} - {round(float(value) * float(total_base), 2)} {keys.get(base)} '
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
