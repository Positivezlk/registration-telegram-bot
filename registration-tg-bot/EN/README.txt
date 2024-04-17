# README

## Description
This Python script utilizes the `telebot` library to create a Telegram bot that manages user registrations and profiles. The bot interacts with users in a chat interface, allowing them to register by providing their name and age, and later view their profile details.

## Features
- **Registration Process**: Users can register by providing their name and age through a series of chat interactions.
- **Profile Viewing**: Registered users can view their profile information, including ID, name, and age.
- **Database Interaction**: The bot stores user registration data in an SQLite database named `database_tg.db`.

## Requirements
- Python 3.x
- `telebot` library
- `sqlite3` library
- `SQLiteStudio` Program

## Installation
1. Clone the repository or download the script.
2. Install the required libraries using pip:
   
   pip install pyTelegramBotAPI
   
3. Run the script with Python:
   
   python your_script_name.py
   

## Configuration
- Replace `'YOUR_BOT_TOKEN'` in the script with your actual Telegram bot token.
- Make sure to have an SQLite database file named `database_tg.db` in the same directory as the script.

## Usage
1. Start the bot by running the script.
2. Interact with the bot on Telegram:
   - New users will be prompted to register.
   - Registered users can view their profile.
   
## Author
Positivezlk (or `qutei`)

For more details, please refer to the [Telebot documentation](https://github.com/eternnoir/pyTelegramBotAPI).