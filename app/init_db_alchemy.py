from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session
from models import UsersTelegram, ChatGpt


engine = create_engine('sqlite:///./db/sqlite3.db', echo=True) # Создаем соединение с базой данных
Base = declarative_base() # Создаем базовый класс для объявления моделей

# Создаем таблицы в базе данных
Base.metadata.create_all(engine)

# Создаем сессию для работы с базой данных
session = Session(engine)


.....

# Пример добавления данных в таблицы
users = UsersTelegram(username='John Doe')
chatgpt = ChatGpt(order_number='123', user=user)

session.add(users)
session.add(chatgpt)
session.commit()


# # Пример запроса с использованием ORM
# result = (
#     session.query(User.username, Order.order_number)
#     .join(Order)
#     .filter(User.id == Order.user_id)
#     .all()
# )

# for username, order_number in result:
#     print(f"Username: {username}, Order Number: {order_number}")