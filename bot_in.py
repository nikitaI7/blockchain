import os
import telebot
from telebot import types
from parse import watch_data, execute_sql_query
import time


def add_to_db(id, message, chain):
    a = str(message.text)
    execute_sql_query("SELECT * FROM users", "insert", [id, a, chain], "maintable")


def watch_addresses(bot, user_id, message):
    a = execute_sql_query(f"SELECT * FROM public.mainTable", "select", "", "")
    counter = 0
    for i in range(len(a)):
        if a[i][0] == user_id:
            counter += 1
            bot.send_message(message.chat.id, text=f"{counter} счёт: {a[i][1]}, блокчейн: {a[i][2]}.")
            time.sleep(1)


blockchain = ""


def bot_in():
    bot = telebot.TeleBot(os.getenv("TELEGA_TOKEN"))

    @bot.message_handler(commands=["start"])  # function /start
    def start(message):
        user_id = message.from_user.id
        print(user_id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Отслеживать состояние моего счета")
        btn2 = types.KeyboardButton("Узнать баланс счета ETH")
        btn3 = types.KeyboardButton("Менеджмент адресов")
        markup.add(btn1, btn2, btn3)
        message.chat.id = user_id
        bot.send_message(message.chat.id,
                         # text="Привет, {0.first_name}! Я тестовый бот для твоего блокчейн счета".format(
                         text="Что же мне сделать,{0.first_name}?".format(
                             message.from_user), reply_markup=markup)
        time.sleep(1)

    @bot.message_handler(content_types=['text'])
    def step_after_start(message):
        blockchains = {"Etherium": "eth",
                       "Goerli": "goerli"}
        assets = {"ETH": "eth",
                  "goerli": "goerli"}
        global blockchain
        user_id = message.from_user.id
        message.chat.id = user_id
        if message.text == "Отслеживать состояние моего счета":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Выбрать блокчейн")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, back)
            bot.send_message(message.chat.id, text="...", reply_markup=markup)
            time.sleep(1)

        elif message.text == "Выбрать блокчейн":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Etherium")
            btn2 = types.KeyboardButton("Goerli")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, btn2, back)
            bot.send_message(message.chat.id, text="...", reply_markup=markup)
            time.sleep(1)

        elif message.text in blockchains.keys():
            for key in blockchains.keys():
                if message.text == key:
                    blockchain = blockchains[key]
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(back)
            msg = bot.send_message(message.chat.id, text="Введите адрес счета", reply_markup=markup)
            time.sleep(1)
            bot.register_next_step_handler(msg, check_message)

        elif message.text == "Узнать баланс счета ETH":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Ввести адрес счета ETH")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, back)
            bot.send_message(message.chat.id, text="...", reply_markup=markup)
            time.sleep(1)

        elif message.text == "Ввести адрес счета ETH":
            msg = bot.send_message(message.chat.id, text="Прошу")
            bot.register_next_step_handler(msg, balance)
            time.sleep(1)

        elif message.text == "Менеджмент адресов":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Показать ваши адреса")
            btn2 = types.KeyboardButton("Удалить адрес")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, btn2, back)
            bot.send_message(message.chat.id, text="...", reply_markup=markup)
            time.sleep(1)

        elif message.text == "Показать ваши адреса":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(back)
            bot.send_message(message.chat.id, text="Ваши счета:", reply_markup=markup)
            watch_addresses(bot, user_id, message)
            time.sleep(1)

        elif message.text == "Удалить адрес":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("ETH")
            btn2 = types.KeyboardButton("goerli")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, btn2, back)
            bot.send_message(message.chat.id, text="Выберите блокчейн", reply_markup=markup)
            time.sleep(1)

        elif message.text in assets.keys():
            for key in assets.keys():
                if message.text == key:
                    blockchain = assets[key]
            print(blockchain)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(back)
            msg = bot.send_message(message.chat.id, text="Введите номер счета", reply_markup=markup)
            bot.register_next_step_handler(msg, delete_address)
            time.sleep(1)

        elif message.text == "Вернуться в главное меню":
            start(message)

    @bot.message_handler(content_types=['text'])
    def delete_address(message):
        sql_delete_query = f"DELETE FROM public.maintable WHERE id = {message.from_user.id} AND address = '{message.text}' AND blockchain = '{blockchain}' "
        execute_sql_query(sql_delete_query, "update", "", "")
        bot.send_message(message.chat.id, text="Ваш счет был успешно удален")
        time.sleep(1)

    @bot.message_handler(content_types=['text'])
    def balance(message):
        user_id = message.from_user.id
        message.chat.id = user_id
        if len(message.text) == 42:
            if message.text.isalnum():
                url = "https://ethereum.api.watchdata.io/node/jsonrpc"
                bal = watch_data("eth_getBalance", [message.text, "latest"], url)
                bot.send_message(message.chat.id, text=bal['result'])
                time.sleep(1)
            else:
                check_message('', message)
        else:
            check_message('', message)

    @bot.message_handler(content_types=['text'])
    def check_message(message):
        user_id = message.from_user.id
        message.chat.id = user_id
        if len(message.text) == 42:
            if message.text.isalnum():
                bot.send_message(message.chat.id, text="Начался мониторинг вашего адреса")
                time.sleep(1)
                add_to_db(user_id, message, blockchain)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Ввести адрес счета")
                back = types.KeyboardButton("Вернуться в главное меню")
                markup.add(btn1, back)
                bot.send_message(message.chat.id, text="Вы ввели недопустимые символы")
                time.sleep(1)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Ввести адрес счета")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, back)
            bot.send_message(message.chat.id, text="Длина вашего адреса не соответствует действительности")
            time.sleep(1)

    bot.polling(none_stop=True, interval=0)


def main():
    bot_in()


if __name__ == "__main__":
    main()
