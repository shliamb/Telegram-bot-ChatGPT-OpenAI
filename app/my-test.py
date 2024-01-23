#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from models import UsersTelegram, engine



Session = sessionmaker(bind=engine)
session = Session()

users = session.query(UsersTelegram).all()
for user in users:
    print(f'User: {user.user_id}, Email: {user.user_username}, id: {user.id}')







# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# Base = declarative_base()

# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     username = Column(String)
#     email = Column(String)

# # Создаем 'engine' и базу данных
# engine = create_engine('sqlite:///:memory:')
# Base.metadata.create_all(engine)
    



# # Создание сессии
# Session = sessionmaker(bind=engine)
# session = Session()

# # Добавление нового пользователя
# new_user = User(username='user1', email='user1@example.com')
# session.add(new_user)
# session.commit()

# # Получение всех пользователей
# users = session.query(User).all()
# for user in users:
#     print(f'User: {user.username}, Email: {user.email}')

# # Обновление данных пользователя
# user_to_update = session.query(User).filter(User.username == 'user1').first()
# user_to_update.email = 'new_email@example.com'
# session.commit()

# # Проверка обновленных данных
# updated_user = session.query(User).filter(User.username == 'user1').first()
# print(f'Updated Email: {updated_user.email}')



# Хорошо, давай попробуем ещё раз, но пошагово и проще.

# Предположим, у нас есть две таблицы: User и Post. Каждый Post связан с User через ForeignKey. Вот как это работает:
    

# from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     username = Column(String)

#     # Это позволяет получить доступ к постам пользователя
#     posts = relationship("Post", back_populates="author")

# class Post(Base):
#     __tablename__ = 'posts'
#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     user_id = Column(Integer, ForeignKey('users.id'))

#     # Это устанавливает связь с пользователем, который создал пост
#     author = relationship("User", back_populates="posts")

# # Подключение к базе данных (здесь мы используем SQLite в памяти)
# engine = create_engine('sqlite:///:memory:')
# Base.metadata.create_all(engine)


# from sqlalchemy.orm import sessionmaker

# # Создание сессии для работы с базой данных
# Session = sessionmaker(bind=engine)
# session = Session()

# # Добавление нового пользователя
# new_user = User(username='user123')
# session.add(new_user)
# session.commit()

# # Добавление нового поста, связанного с пользователем
# new_post = Post(title='My First Post', user_id=new_user.id)
# session.add(new_post)
# session.commit()

# # Получение и вывод постов и их авторов
# posts = session.query(Post).all()
# for post in posts:
#     print(f'Post Title: {post.title}, Author: {post.author.username}')


# Модели: User и Post связаны через ForeignKey и relationship.
# Добавление данных: Создаем пользователя и пост, связанный с этим пользователем.
# Запросы: Получаем все посты и выводим их названия вместе с именами пользователей.
# Это базовый пример взаимодействия с связанными данными в SQLAlchemy.