import time
import requests
from logging_bot import logger

while True:
    try:
        pass
        print("Погнали...")
        from tele_bot import start_bot
        start_bot(none_stop=True, timeout=60)
        break
    except requests.exceptions.ReadTimeout:
        logger.error("Request timeout exceeded. Restart...")
        print("Request timeout exceeded. Restart...")
        time.sleep(5)
    # except Exception as e:
    #     logger.exception("Произошла непредвиденная ошибка:")
    #     print(f"Error : {e}")
    #     break










# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, create_engine
# import requests
# import json
# import logging
# import time
# import os
#import telebot
# from telebot import types
#from keys import api_key
# from sqlalchemy.orm import relationship, sessionmaker
# from models import UsersTelegram, engine

################################ Bot #####

# # Вызов меню /start
# @bot.message_handler(commands=['start'])
# def start(context):
#     bot.send_message(context.chat.id, text=f"Привет, {context.from_user.username}! Добро пожаловать в бота.")
#     user_id = context.from_user.id
#     read_user(user_id)


#bot.polling(none_stop=True, timeout=60) 





    # user_id = message.from_user.id
    # user_first_name = message.from_user.first_name  # Имя пользователя
    # user_last_name = message.from_user.last_name  # Фамилия пользователя (может быть None)
    # user_username = message.from_user.username  # Юзернейм пользователя (может быть None)
    # chat_id = message.chat.id


# import sqlite3

# ############################# Work to db ####################
# # Функция для подключения к базе данных
# def get_db_connection():
#     database_path = './db/sqlite3.db'
#     return sqlite3.connect(database_path)

# # Чтение данных пользователя
# def read_user_data(user_id):
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM users_telegram WHERE user_id = ?", (user_id,))
#         rows = cursor.fetchall()
#         return rows

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