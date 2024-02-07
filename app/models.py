#from keys import pass_psgresql # {pass_psgresql}
import datetime
from sqlalchemy import ForeignKey
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship


DATABASE_URL = f"postgresql+asyncpg://admin:12345@localhost:5432/my_database"
engine = create_async_engine(DATABASE_URL) # Создание асинхронного движка для работы с базой данных
Base = declarative_base() # Создание базового класса для объявления моделей
Column = sqlalchemy.Column


# if has access to base in the future - None
class UsersBase(Base):
    __tablename__ = 'users_db'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    username = sqlalchemy.Column(sqlalchemy.String(50), nullable=False, unique=True)
    password = Column(sqlalchemy.String(100), nullable=False)
    email = Column(sqlalchemy.String(100), nullable=True, unique=True)



# Users Telegram - Main
class UsersTelegram(Base):
    __tablename__ = 'users_telegram'
    id = Column(sqlalchemy.BigInteger, primary_key=True, unique=True, nullable=False, index=True)
    name = Column(sqlalchemy.String(50), nullable=True)
    full_name = Column(sqlalchemy.String(50), nullable=True)
    first_name = Column(sqlalchemy.String(50), nullable=True)
    last_name = Column(sqlalchemy.String(50), nullable=True)
    chat_id = Column(sqlalchemy.BigInteger, nullable=True) # если не пользователь, а от лица группы то свой id, если  user то user_id
    is_admin = Column(sqlalchemy.Boolean, default=False, server_default="False", nullable=False) # Админ ли
    is_block = Column(sqlalchemy.Boolean, default=False, server_default="False", nullable=False) # За блокирован ли
    is_good = Column(sqlalchemy.Integer, default=3, server_default="3", nullable=False) # Рейтинг, хз зачем, посмотрим, может скидки.. Без запрета null, default не выставиться
    ###
    settings = relationship("Settings", back_populates="userstelegram", uselist=False)
    stat = relationship("Statistics")
    discussion = relationship("Discussion", back_populates="userstelegram", uselist=False)



# Settings - One-to-One
class Settings(Base):
    __tablename__ = 'settings'
    id = Column(sqlalchemy.BigInteger, ForeignKey('users_telegram.id'), primary_key=True)
    temp_chat = Column(sqlalchemy.Float, default=0.7, server_default="0.7", nullable=False)  # 0 - 1 консервативность - разнообразие
    frequency = Column(sqlalchemy.Float, default=0.5, server_default="0.5", nullable=False) # 0 - 1 допускает повторение слов и фраз в рамках данного ответа, 
    presence = Column(sqlalchemy.Float, default=0.5, server_default="0.5", nullable=False) # 0 - 1 допускает повторение слов и фраз из прошлых ответов
    flag_stik = Column(sqlalchemy.Boolean, default=False, server_default="False", nullable=False)
    all_count = Column(sqlalchemy.Integer, default=0, server_default="0",  nullable=False) # Колличество вопросов за все время
    all_token = Column(sqlalchemy.Integer, default=0, server_default="0",  nullable=False) # Всего токенов затраченых за все время
    the_gap = Column(sqlalchemy.Float, default=0.05, server_default="0.05", nullable=False) # Выбранное время хранения диалога
    set_model = Column(sqlalchemy.String(50), default="gpt-3.5-turbo-0613", server_default="gpt-3.5-turbo-0613",  nullable=False) # Выбранная модель чата
    give_me_money = Column(sqlalchemy.Float, default=0, server_default="0", nullable=False) # З
    money = Column(sqlalchemy.Float, default=100, server_default="100", nullable=False)  # Денег на счету
    all_in_money = Column(sqlalchemy.Float, default=0, server_default="0", nullable=False) # Всего денег внесено за все время
    ###
    userstelegram = relationship("UsersTelegram", back_populates="settings")

# Saved answers and questions - One-to-One
class Discussion(Base):
    __tablename__ = 'discussion'
    id = Column(sqlalchemy.BigInteger, ForeignKey('users_telegram.id'), primary_key=True)
    discus = Column(sqlalchemy.String(7000))
    timestamp = Column(sqlalchemy.DateTime, onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow, nullable=False) # Каждый раз обновляется, при изменениях в ячейке
    ###
    userstelegram = relationship("UsersTelegram", back_populates="discussion")


# Save data exchange USD to RUB  first at day - None
class Exchange(Base):
    __tablename__ = 'exchange'
    id = Column(sqlalchemy.Integer, primary_key=True)
    timestamp = Column(sqlalchemy.DateTime, onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow, nullable=False) # Каждый раз обновляется, при изменениях в ячейке
    rate = Column(sqlalchemy.Float(30), default=100, server_default="100", nullable=False)
    ###


# User spending statistics - One-to-many
class Statistics(Base):
    __tablename__ = 'statistics'
    id = Column(sqlalchemy.Integer, primary_key=True)
    time = Column(sqlalchemy.DateTime, onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow, nullable=False) # Каждый раз обновляется сама, при изменениях в ячейке
    use_model = Column(sqlalchemy.String(50), nullable=False) # Использованная модель
    sesion_token = Column(sqlalchemy.Integer, default=0, server_default="0",  nullable=False) # Использованно токенов
    price_1_tok = Column(sqlalchemy.Float, default=0, server_default="0", nullable=False) # Цена токена, если менялась, то будет видно
    price_sesion_tok = Column(sqlalchemy.Float, default=0, server_default="0", nullable=False) #  Вся цена
    ###
    users_telegram_id = Column(sqlalchemy.BigInteger, ForeignKey("users_telegram.id"), index=True) # id user telegram





# Build Table to DB
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Creature session interactions to DB
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# Функция для получения асинхронной сессии
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session