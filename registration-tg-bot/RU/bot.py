import sqlite3
import telebot
from telebot import types

bot = telebot.TeleBot('YOU_API_TOKEN')


@bot.message_handler(commands=['start'])
def say_hello(message):
    # Подключение к базе данных SQLite
    db = sqlite3.connect('database_tg.db')
    cursor = db.cursor()

    # Получение всех Telegram ID из базы данных
    cursor.execute('SELECT FtgID_user FROM Ttg_users')
    tg_ids = [row[0] for row in cursor.fetchall()]
    db.close()

    # Проверка, зарегистрирован ли пользователь
    if not message.chat.id in tg_ids:
        button = types.InlineKeyboardButton('Пройти регистрацию', callback_data='pass_reg')
        markup = types.InlineKeyboardMarkup()
        markup.add(button)
        bot.send_message(message.chat.id, 'Здравствуйте. Добро пожаловать на регистрацию! '
                                          'Пройти её можно, нажав ниже на кнопку', reply_markup=markup)
    else:
        button = types.InlineKeyboardButton('Посмотреть профиль', callback_data='check_profile')
        markup = types.InlineKeyboardMarkup()
        markup.add(button)
        bot.send_message(message.chat.id, 'Вы уже прошли регистрацию. Желаете посмотреть профиль?',
                         reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call):
    if call.data == 'pass_reg':
        registration_name(call.message)
    elif call.data == 'check_profile':
        profile(call.message)


def registration_name(message):
    bot.send_message(message.chat.id, 'Как вас зовут?')
    bot.register_next_step_handler(message, registration_age)


def registration_age(message):
    name = message.text
    bot.send_message(message.chat.id, f'Приятно познакомиться, <b>{name}</b>, сколько вам лет?', parse_mode='HTML')
    bot.register_next_step_handler(message, lambda message: finish_registration(message, name))


def finish_registration(message, name):
    age = message.text
    # Подключение к базе данных SQLite
    db = sqlite3.connect('database_tg.db')
    cursor = db.cursor()

    # Вставка данных пользователя в базу данных
    cursor.execute('INSERT INTO Ttg_users VALUES(NULL, ?, ?, ?)', (name, age, message.chat.id))
    db.commit()
    db.close()
    button = types.InlineKeyboardButton('Посмотреть профиль', callback_data='check_profile')
    markup = types.InlineKeyboardMarkup()
    markup.add(button)
    bot.send_message(message.chat.id, 'Регистрация завершена! Благодарим за принятие участия! :)',
                     reply_markup=markup)


def profile(message):
    # Подключение к базе данных SQLite
    db = sqlite3.connect('database_tg.db')
    cursor = db.cursor()

    # Получение данных пользователя из базы данных
    cursor.execute('SELECT * FROM Ttg_users WHERE FtgID_user = ?', (message.chat.id,))
    user_data = cursor.fetchone()

    # Получение общего количества пользователей в базе данных
    cursor.execute('SELECT COUNT(Fid_user) FROM Ttg_users')
    user_count = cursor.fetchone()
    db.close()

    if user_data:
        bot.send_message(message.chat.id, f"<b>-----Данные пользователя:-----</b>\n<b>- ID</b>: "
                                          f"<u>{user_data[0]}</u>\n-----------------------------------\n<b>- Имя</b>: "
                                          f"<u>{user_data[1]}</u>\n-----------------------------------\n"
                                          f"<b>- Возраст</b>: <u>{user_data[2]}</u>\n\n"
                                          f"Общее кол-во участвующих: {user_count[0]}", parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, "Пользователь с таким Telegram ID не найден в базе данных.",
                         parse_mode='HTML')


# Начало получения сообщений
bot.polling(none_stop=True)
