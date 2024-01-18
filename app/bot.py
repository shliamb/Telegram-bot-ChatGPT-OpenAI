import os
import time
import telebot
from telebot import types
import requests
import json
import logging
import sqlite3

#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from models import UsersTelegram, engine


Session = sessionmaker(bind=engine)
session = Session()
users = session.query(UsersTelegram).all()
for user in users:
    print(f'User: {user.user_id}, Email: {user.user_username}, id: {user.id}')





############################## API Key Telegram Bot  ##########
token = os.environ.get('TELEGRAM_BOT_CHATGPT_API_KEY')
bot = telebot.TeleBot(token)

############################# Work to db ####################
# Функция для подключения к базе данных
def get_db_connection():
    database_path = './db/sqlite3.db'
    return sqlite3.connect(database_path)

# Чтение данных пользователя
def read_user_data(user_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users_telegram WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        return rows
        #for row in rows:
        #    print(f" {row} \n")

def insert_user_data(user_id, user_first_name, user_last_name, user_username):
    database_path = './db/sqlite3.db'
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users_telegram WHERE user_id = ?", (user_id,)) # Выдаст user_id если найдет совпадение, и ничего не выдаст если не найдет
    existing_user = cursor.fetchone() # cursor.fetchone() извлекает эту одну строку (кортеж) из результата запроса и присваивает ее переменной existing_user
    if existing_user is None:
        cursor.execute("INSERT INTO users_telegram (user_id, user_first_name, user_last_name, user_username) VALUES (?, ?, ?, ?)", (user_id, user_first_name, user_last_name, user_username))
        conn.commit() # фиксация изменений db
    else:
        print("\nПользователь с таким user_id уже существует\n")
    conn.close()

# # Вставка данных пользователя
# def insert_user_data(user_id, user_first_name, user_last_name, user_username):
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT user_id FROM users_telegram WHERE user_id = ?", (user_id,))
#         if cursor.fetchone() is None:
#             cursor.execute("INSERT INTO users_telegram (user_id, user_first_name, user_last_name, user_username) VALUES (?, ?, ?, ?)", (user_id, user_first_name, user_last_name, user_username))
#             conn.commit()
#         else:
#             print("Пользователь с таким user_id уже существует")

################################ Bot #####

# Вызов меню /start
@bot.message_handler(commands=['start'])
def start(context):
    bot.send_message(context.chat.id, text=f"Привет, {context.from_user.username}! Добро пожаловать в бота.")
    #insert_user_data(context.from_user.id, context.from_user.first_name, context.from_user.last_name, context.from_user.username)
    #data_user = read_user_data(context.from_user.id)
    #print(f"Data user: {data_user}")
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # users = session.query(UsersTelegram).all()
    # for user in users:
    #     #print(f'User: {user.username}, Email: {user.email}')
    #     print(user)




bot.polling(none_stop=True, timeout=10) 





    # user_id = message.from_user.id
    # user_first_name = message.from_user.first_name  # Имя пользователя
    # user_last_name = message.from_user.last_name  # Фамилия пользователя (может быть None)
    # user_username = message.from_user.username  # Юзернейм пользователя (может быть None)
    # chat_id = message.chat.id
