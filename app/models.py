from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, create_engine
from sqlalchemy.orm import relationship, sessionmaker
import datetime


engine = create_engine('sqlite:///./db/sqlite3.db') # Создаем соединение с базой данных
Base = declarative_base() # Создаем базовый класс для объявления моделей


# if has access to base
class UsersBase(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True, unique=True)

# Users Telegram - Main
class UsersTelegram(Base):
    __tablename__ = 'users_telegram'
    id = Column(Integer, primary_key=True, unique=True, nullable=False, index=True) # user_id unique
    user_username = Column(String(50), nullable=True)
    user_first_name = Column(String(50), nullable=True)
    user_last_name = Column(String(50), nullable=True)
    chat_id = Column(Integer, nullable=True) # если не пользователь, а от лица группы то свой id, если  user то user_id
    is_user_admin = Column(Boolean, default=False, server_default="False", nullable=False) # Админ ли
    is_user_block = Column(Boolean, default=False, server_default="False", nullable=False) # За блокирован ли
    is_user_good = Column(Integer, default=3, server_default="3", nullable=False) # Рейтинг, хз зачем, посмотрим, может скидки.. Без запрета null, default не выставиться
    ###
    chatgpt = relationship("ChatGpt", back_populates="userstelegram", uselist=False)
    statistic = relationship("Statistic")
    saved_questions = relationship("SavedQuestion")

# Users settings ChatGPT - One-to-One
class ChatGpt(Base):
    __tablename__ = 'chatgpt_setings'
    id = Column(Integer, ForeignKey('users_telegram.id'), primary_key=True)
    temp_chat = Column(Float, default=0.7, server_default="0.7", nullable=False)
    lang_chat = Column(String(15), default="RU", server_default="RU",  nullable=False)
    count_req_chat = Column(Integer, default=0, server_default="0",  nullable=False) # Колличество вопросов за все время
    used_token_chat = Column(Integer, default=0, server_default="0",  nullable=False) # Всего токенов затраченых за все время
    limit_token_chat = Column(Integer, default=0, server_default="0",  nullable=False) # Лимит токенов - не использовать вскоре
    the_gap = Column(Float, default=0.05, server_default="0.05", nullable=False) # Выбранное время хранения диалога
    model_id = Column(String(50), default="gpt-3.5-turbo", server_default="gpt-3.5-turbo",  nullable=False) # Выбранная модель чата
    money_user = Column(Float, default=25, server_default="25", nullable=False)  # Денег на счету
    total_spent_money = Column(Float, default=0, server_default="0", nullable=False) # Всего денег внесено за все время
    ###
    userstelegram = relationship("UsersTelegram", back_populates="chatgpt")

# User spending statistics - One-to-many
class Statistic(Base):
    __tablename__ = 'statistics'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow, nullable=False) # Каждый раз обновляется сама, при изменениях в ячейке
    model = Column(String(50), nullable=False) # Использованная модель
    used_token = Column(Integer, default=0, server_default="0",  nullable=False) # Использованно токенов
    cost_token = Column(Float, default=0, server_default="0", nullable=False) # Цена токена, если менялась, то будет видно
    entire_cost = Column(Float, default=0, server_default="0", nullable=False) #  Вся цена
    ###
    users_telegram_id = Column(Integer, ForeignKey("users_telegram.id"), index=True) # id user telegram



# Saved answers and questions - One-to-many
class SavedQuestion(Base):
    __tablename__ = 'saved_questions'
    id = Column(Integer, primary_key=True)
    question_text = Column(String(7000))
    timestamp = Column(DateTime, onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow, nullable=False) # Каждый раз обновляется, при изменениях в ячейке
    ###
    users_telegram_id = Column(Integer, ForeignKey("users_telegram.id"), index=True)

# Save data exchange USD to RUB  first at day - None
class Exchange(Base):
    __tablename__ = 'exchange'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow, nullable=False) # Каждый раз обновляется, при изменениях в ячейке
    price = Column(Float(30), default=100, server_default="100", nullable=False)
    ###

Base.metadata.create_all(engine) # Создаем таблицы в базе данных