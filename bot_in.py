import telebot
from telebot import types
import psycopg2
from psycopg2 import OperationalError


def create_connection(db,user,user_password,db_host):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db,
            user=user,
            password=user_password,
            host=db_host,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def Answer(id,message):
    a =str(message.text)
    conn = create_connection('blockchainbot','blockchainbot','blockchainbot123','185.137.234.101')
    select_db ="SELECT * FROM users"
    insert_query = (
        f"INSERT INTO firsttable VALUES {id,a}"
    )

    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(insert_query, select_db)






    print(message.text)


def BotIn():
    bot = telebot.TeleBot('5214289967:AAEEMgnpnVIxihuOLmYOs1IofohaG2EBsAg')

    @bot.message_handler(commands=["start"])  # function /start
    def start(message):
        user_id = message.from_user.id
        print(user_id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Отслеживать состояние моего счета")
        btn2 = types.KeyboardButton("❓ Задать вопрос")
        markup.add(btn1, btn2)
        message.chat.id = user_id
        bot.send_message(message.chat.id,
                         text="Привет, {0.first_name}! Я тестовый бот для твоего блокчейн счета".format(
                             message.from_user), reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def func(message):
        user_id = message.from_user.id
        message.chat.id = user_id
        if message.text == "Отслеживать состояние моего счета":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Ввести адрес счета")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, back)

            bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)

        elif message.text == "Ввести адрес счета":
            msg = bot.send_message(message.chat.id, text="Прошу")
            bot.register_next_step_handler(msg, funct)

        elif message.text == "Вернуться в главное меню":
            start(message)

    def funct(message):
        user_id = message.from_user.id
        message.chat.id = user_id
        if len(message.text) == 42:
            if message.text.isalnum():
                bot.send_message(message.chat.id, text="Начался мониторинг вашего адреса")
                # add to db
                Answer(user_id,message)

            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Ввести адрес счета")
                back = types.KeyboardButton("Вернуться в главное меню")
                markup.add(btn1, back)
                bot.send_message(message.chat.id, text="Вы ввели недопустимые символы")
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Ввести адрес счета")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, back)
            bot.send_message(message.chat.id, text="Длина вашего адреса не соответствует действительности")

    bot.polling(none_stop=True, interval=0)


def main():
    BotIn()


if __name__ == "__main__":
    main()