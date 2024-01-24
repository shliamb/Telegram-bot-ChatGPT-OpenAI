import telebot
from telebot import types
from .keys import token, api_key
from sqlalchemy.orm import relationship, sessionmaker
from models import UsersTelegram, engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, create_engine
# import requests
# import json
# import logging
# import time
# import os


bot = telebot.TeleBot(token)

############################# Work to db ####################
# Функция для подключения к базе данных
Session = sessionmaker(bind=engine)
session = Session()

# Чтение 
def read_user(absd):
    users = session.query(UsersTelegram).filter(UsersTelegram.user_id == absd).all()
    for user in users:
        print(f'User: {user.user_id}, Email: {user.user_username}, id: {user.id}')


# Запись
def add_user(user_id, user_username):
    new_user = UsersTelegram(user_id=user_id, user_username=user_username)
    session.add(new_user)
    session.commit()







################################ Bot #####

# Вызов меню /start
@bot.message_handler(commands=['start'])
def start(context):
    bot.send_message(context.chat.id, text=f"Привет, {context.from_user.username}! Добро пожаловать в бота.")
    user_id = context.from_user.id
    read_user(user_id)


bot.polling(none_stop=True, timeout=10) 





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