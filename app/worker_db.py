from keys import pass_psgresql
import logging
import asyncio
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Base, UsersTelegram, Settings, Discussion
from sqlalchemy import select, insert, update, func

async def create_async_engine_and_session():
    engine = create_async_engine(f"postgresql+asyncpg://admin:{pass_psgresql}@localhost:5432/my_database") # echo=True - вывод логирования
    async_session = sessionmaker(bind=engine, class_=AsyncSession)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return async_session

#logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
#logging.basicConfig(level=logging.INFO, filename='log/app.log', filemode='a', format='%(levelname)s - %(asctime)s - %(name)s - %(message)s',) # При деплое активировать логирование в файл


#### USER TELEGRAM PROPERTY ####
# Read User Telegram Data
async def get_user_by_id(id):
    async_session = await create_async_engine_and_session()
    async with async_session() as session:
        # Выполняем запрос на выборку данных пользователя из таблицы UsersTelegram по переданному идентификатору
        query = select(UsersTelegram).filter(UsersTelegram.id == id)
        result = await session.execute(query)
        # Получаем первую строку, которая соответствует запросу
        data = result.scalar_one_or_none()  # - это метод SQLAlchemy, который возвращает ровно один результат из результата запроса или None, если запрос не вернул ни одного результата.
        return data or None

# Update User Telegram
async def update_user(id, updated_data):
    async_session = await create_async_engine_and_session()
    confirmation = False
    async with async_session() as session:
        try:
            query = update(UsersTelegram).where(UsersTelegram.id == id).values(**updated_data)
            await session.execute(query)
            await session.commit()
            confirmation = True
        except Exception as e:
            logging.error(f"Failed to update user: {e}")
    return confirmation

# Add User Telegram to DB
async def adding_user(user_data):
    async_session = await create_async_engine_and_session()
    confirmation = False
    async with async_session() as session:
        try:
            query = insert(UsersTelegram).values(**user_data)
            await session.execute(query)
            await session.commit()
            confirmation = True
        except Exception as e:
            logging.error(f"Failed to add user: {e}")
    return confirmation




#### SETTINGS CHATGPT ####
# Read Settings
async def get_settings(id):
    async_session = await create_async_engine_and_session()
    async with async_session() as session:
        query = select(Settings).filter(Settings.id == id)
        result = await session.execute(query)
        data = result.scalar_one_or_none() 
        return data or None

# Update Settings 
async def update_settings(id, updated_data):
    async_session = await create_async_engine_and_session()
    confirmation = False
    async with async_session() as session:
        try:
            query = update(Settings).where(Settings.id == id).values(**updated_data)
            await session.execute(query)
            await session.commit()
            confirmation = True
        except Exception as e:
            logging.error(f"Failed to update settings: {e}")
    return confirmation

# Add to settings User ID
async def add_settings(id):
    async_session = await create_async_engine_and_session()
    confirmation = False
    async with async_session() as session:
        try:
            data = {"id": id}
            query = insert(Settings).values(**data)
            await session.execute(query)
            await session.commit()
            confirmation = True
        except Exception as e:
            logging.error(f"Failed to add id settings: {e}")
    return confirmation




####  DISCUSSION ####
# Read Discussion
async def get_discussion(id):
    async_session = await create_async_engine_and_session()
    async with async_session() as session:
        query = select(Discussion).filter(Discussion.id == id)
        result = await session.execute(query)
        data = result.scalar_one_or_none() 
        return data or None

# Update Discussion 
async def update_discussion(id, updated_data):
    async_session = await create_async_engine_and_session()
    confirmation = False
    async with async_session() as session:
        try:
            query = update(Discussion).where(Discussion.id == id).values(**updated_data)
            await session.execute(query)
            await session.commit()
            confirmation = True
        except Exception as e:
            logging.error(f"Failed to update Discussion: {e}")
    return confirmation

# Add id to Discussion Table
async def add_discussion(id):
    async_session = await create_async_engine_and_session()
    confirmation = False
    async with async_session() as session:
        try:
            data = {"id": id}
            query = insert(Discussion).values(**data)
            await session.execute(query)
            await session.commit()
            confirmation = True
        except Exception as e:
            logging.error(f"Failed to add id Discussion: {e}")
    return confirmation


