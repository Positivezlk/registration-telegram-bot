import sqlite3
import telebot
from telebot import types

bot = telebot.TeleBot('YOUR_BOT_TOKEN')


@bot.message_handler(commands=['start'])
def say_hello(message):
    # Connect to the SQLite database
    db = sqlite3.connect('database_tg.db')
    cursor = db.cursor()

    # Retrieve all Telegram IDs from the database
    cursor.execute('SELECT FtgID_user FROM Ttg_users')
    tg_ids = [row[0] for row in cursor.fetchall()]
    db.close()

    # Check if the user is already registered
    if not message.chat.id in tg_ids:
        button = types.InlineKeyboardButton('Proceed with registration', callback_data='pass_reg')
        markup = types.InlineKeyboardMarkup()
        markup.add(button)
        bot.send_message(message.chat.id, 'Hello. Welcome to the registration! '
                                          'You can proceed by clicking the button below', reply_markup=markup)
    else:
        button = types.InlineKeyboardButton('View profile', callback_data='check_profile')
        markup = types.InlineKeyboardMarkup()
        markup.add(button)
        bot.send_message(message.chat.id, 'You have already completed your registration. '
                                          'Would you like to view your profile?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call):
    if call.data == 'pass_reg':
        registration_name(call.message)
    elif call.data == 'check_profile':
        profile(call.message)


def registration_name(message):
    bot.send_message(message.chat.id, 'What is your name?')
    bot.register_next_step_handler(message, registration_age)


def registration_age(message):
    name = message.text
    bot.send_message(message.chat.id, f'Nice to meet you, <b>{name}</b>. How old are you?', parse_mode='HTML')
    bot.register_next_step_handler(message, lambda message: finish_registration(message, name))


def finish_registration(message, name):
    age = message.text
    # Connect to the SQLite database
    db = sqlite3.connect('database_tg.db')
    cursor = db.cursor()

    # Insert the user's data into the database
    cursor.execute('INSERT INTO Ttg_users VALUES(NULL, ?, ?, ?)', (name, age, message.chat.id))
    db.commit()
    db.close()

    button = types.InlineKeyboardButton('View profile', callback_data='check_profile')
    markup = types.InlineKeyboardMarkup()
    markup.add(button)
    bot.send_message(message.chat.id, 'Registration completed! Thank you for participating! :)',
                     reply_markup=markup)


def profile(message):
    # Connect to the SQLite database
    db = sqlite3.connect('database_tg.db')
    cursor = db.cursor()

    # Retrieve the user's data from the database
    cursor.execute('SELECT * FROM Ttg_users WHERE FtgID_user = ?', (message.chat.id,))
    user_data = cursor.fetchone()

    # Get the total number of users in the database
    cursor.execute('SELECT COUNT(Fid_user) FROM Ttg_users')
    user_count = cursor.fetchone()
    db.close()

    if user_data:
        bot.send_message(message.chat.id, f"<b>-----User Data:-----</b>\n<b>- ID</b>: "
                                          f"<u>{user_data[0]}</u>\n-----------------------------------\n<b>- Name</b>: "
                                          f"<u>{user_data[1]}</u>\n-----------------------------------\n"
                                          f"<b>- Age</b>: <u>{user_data[2]}</u>\n\n"
                                          f"Total participants: {user_count[0]}", parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, "User with this Telegram ID was not found in the database.",
                         parse_mode='HTML')


# Start polling for messages
bot.polling(none_stop=True)
