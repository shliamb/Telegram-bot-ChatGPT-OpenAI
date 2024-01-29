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

# users Telegram
class UsersTelegram(Base):
    __tablename__ = 'users_telegram'
    id = Column(Integer, primary_key=True, unique=True, nullable=False, index=True) # user_id unique
    user_username = Column(String(50), nullable=True)
    user_first_name = Column(String(50), nullable=True)
    user_last_name = Column(String(50), nullable=True)
    chat_id = Column(Integer, nullable=True) # если не пользователь, а от лица группы то свой id, если  user то user_id
    is_user_admin = Column(Boolean, default=False, server_default="False", nullable=False) # default срабатывает только так
    is_user_block = Column(Boolean, default=False, server_default="False", nullable=False)
    is_user_good = Column(Integer, default=3, server_default="3", nullable=False) # Без запрета null, default не выставиться
    ###
    chatgpt = relationship("ChatGpt", back_populates="userstelegram", uselist=False)
    saved_questions = relationship("SavedQuestion")

# users gpt settings
class ChatGpt(Base):
    __tablename__ = 'chatgpt_setings'
    id = Column(Integer, ForeignKey('users_telegram.id'), primary_key=True)
    temp_chat = Column(Float, default=0.7, server_default="0.7", nullable=False)
    lang_chat = Column(String(15), default="RU", server_default="RU",  nullable=False)
    count_req_chat = Column(Integer, default=0, server_default="0",  nullable=False)
    used_token_chat = Column(Integer, default=0, server_default="0",  nullable=False)
    limit_token_chat = Column(Integer, default=0, server_default="0",  nullable=False)
    the_gap = Column(Float, default=0.15, server_default="0.15", nullable=False)
    model_id = Column(String(50), default="gpt-3.5-turbo", server_default="gpt-3.5-turbo",  nullable=False) 
    ###
    userstelegram = relationship("UsersTelegram", back_populates="chatgpt")

# SavedQuestion
class SavedQuestion(Base):
    __tablename__ = 'saved_questions'
    id = Column(Integer, primary_key=True)
    question_text = Column(String(7000))
    timestamp = Column(DateTime, onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow, nullable=False) # Каждый раз обновляется, при изменениях в таблице
    ###
    users_telegram_id = Column(Integer, ForeignKey("users_telegram.id"), index=True)


Base.metadata.create_all(engine) # Создаем таблицы в базе данных