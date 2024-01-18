from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, create_engine
from sqlalchemy.orm import relationship, sessionmaker
import datetime


Base = declarative_base()

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
    id = Column(Integer, primary_key=True) # Primari_key - уникален по умолчанию
    name = Column(String(50), nullable=True)
    user_id = Column(Integer, unique=True, nullable=False) # user_id unique
    user_first_name = Column(String(50), nullable=True)
    user_last_name = Column(String(50), nullable=True)
    user_username = Column(String(50), nullable=True)
    chat_id = Column(Integer, nullable=True) # если не пользователь, а от лица группы то свой id, если  user то user_id
    is_user_admin = Column(Boolean, default=False, server_default="False", nullable=False) # default срабатывает только так
    is_user_block = Column(Boolean, default=False, server_default="False", nullable=False)
    is_user_good = Column(Integer, default=3, server_default="3", nullable=False) # Без запрета null, default не выставиться
    ###
    chatgpt = relationship("ChatGpt", back_populates="userstelegram", uselist=False)
    saved_questions = relationship("SavedQuestion")

# user's gpt settings
class ChatGpt(Base):
    __tablename__ = 'chatgpt_setings'
    id = Column(Integer, ForeignKey('users_telegram.id'), primary_key=True)
    temp_chat = Column(Float, default=0.7, server_default="0.7", nullable=False)
    lang_chat = Column(String(15), default="RU", server_default="RU",  nullable=False)
    count_req_chat = Column(Integer, nullable=True)
    used_token_chat = Column(Integer, nullable=True)
    limit_token_chat = Column(Integer, nullable=True)
    ###
    model_id = Column(Integer, ForeignKey("models_chat.id"), default=1, server_default="1",  nullable=False)  # Связь с ModelsChat. Внешний ключ, автоматом установил 2 id из таблицы, куда скриптом init_db добавятся модели gpt
    patch_chat = Column(Integer, ForeignKey("patch_chat.id"), default=1, server_default="1",  nullable=False)
    userstelegram = relationship("UsersTelegram", back_populates="chatgpt")

# models_chat gpt choice
class ModelsChat(Base):
    __tablename__ = 'models_chat'
    id = Column(Integer, primary_key=True)
    models_chat = Column(String(30), nullable=True)
    ###
    chatgpt_setings = relationship("ChatGpt")

# patch_chat choice
class PatchChat(Base):
    __tablename__ = 'patch_chat'
    id = Column(Integer, primary_key=True)
    patch_chat = Column(String(100), nullable=True)
    ###
    chatgpt_setings = relationship("ChatGpt")

# SavedQuestion
class SavedQuestion(Base):
    __tablename__ = 'saved_questions'
    id = Column(Integer, primary_key=True)
    question_text = Column(String(2000))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    ###
    users_telegram_id = Column(Integer, ForeignKey("users_telegram.id"))
    answer = relationship("SavedAnswer", back_populates="question", uselist=False)

# SavedAnswer
class SavedAnswer(Base):
    __tablename__ = 'saved_answer'
    id = Column(Integer, primary_key=True)
    answer_text = Column(String(2000))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    ###
    question_id = Column(Integer, ForeignKey("saved_questions.id"))
    question = relationship("SavedQuestion", back_populates="answer")



# Создаем 'engine' и базу данных
engine = create_engine('sqlite:///./db/sqlite3.db')
Base.metadata.create_all(engine)