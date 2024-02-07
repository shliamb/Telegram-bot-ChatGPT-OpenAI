from keys import pass_psgresql
import logging
import asyncio
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Base, UsersTelegram, Settings, Discussion, Exchange, Statistics
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
            logging.info(f"update_user {id}")
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
            logging.info("adding_user")
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
            logging.info(f"Update Settings {id}")
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
            logging.info(f"add_settings {id}")
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
            logging.info(f"Update Discussion {id}")
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
            logging.info(f"add_discussion {id}")
        except Exception as e:
            logging.error(f"Failed to add id Discussion: {e}")
    return confirmation


#### ECXHANGE ####
# Read exchange
async def get_exchange():
    id = 1
    async_session = await create_async_engine_and_session()
    async with async_session() as session:
        query = select(Exchange).filter(Exchange.id == id)
        result = await session.execute(query)
        data = result.scalar_one_or_none() 
        return data or None

# Add_exchange
async def add_exchange(data):
    async_session = await create_async_engine_and_session()
    confirmation = False
    async with async_session() as session:
        try:
            query = insert(Exchange).values(**data)
            await session.execute(query)
            await session.commit()
            confirmation = True
            logging.info("Add_exchange")
        except Exception as e:
            logging.error(f"Failed to add Excheange rait: {e}")
    return confirmation


# Update_exchange 
async def update_exchange(id, updated_data):
    async_session = await create_async_engine_and_session()
    confirmation = False
    async with async_session() as session:
        try:
            query = update(Exchange).where(Exchange.id == id).values(**updated_data)
            await session.execute(query)
            await session.commit()
            confirmation = True
            logging.info("Update_exchange")
        except Exception as e:
            logging.error(f"Failed to update Exchange rait: {e}")
    return confirmation




#### STATISTICS ####
# Add statistics
async def add_statistic(data):
    async_session = await create_async_engine_and_session()
    confirmation = False
    async with async_session() as session:
        try:
            query = insert(Statistics).values(**data)
            await session.execute(query)
            await session.commit()
            confirmation = True
            logging.info("Add a one statistics line to table")
        except Exception as e:
            logging.error(f"Failed to add statistics: {e}")
    return confirmation


# Read Statistics on id all 30 line
async def get_last_30_statistics(id):
    async_session = await create_async_engine_and_session()
    async with async_session() as session:
        query = (
            select(Statistics)
            .filter(Statistics.users_telegram_id == id)
            .order_by(Statistics.time.desc())  # Сортировка по убыванию даты
            .limit(30)  # Ограничение на количество строк
        )
        result = await session.execute(query)
        data = result.scalars().all()  # Получение всех строк
        return data
