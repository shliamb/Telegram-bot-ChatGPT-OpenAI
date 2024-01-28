# импортируем модуль sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

# задаем язык и количество предложений в резюме
LANGUAGE = 'russian'
SENTENCES_COUNT = 2

# создаем парсер и суммаризатор
parser = PlaintextParser.from_string('Асинхронность - это способ выполнения задач, при котором они могут быть запущены одновременно и выполняться независимо друг от друга. Она позволяет программе продолжать работать, не ожидая завершения каждой задачи. Это особенно полезно при работе с долгими или ресурсоемкими операциями, такими как загрузка данных из Интернета или выполнение сложных вычислений, позволяя приложению оставаться отзывчивым и эффективным.', Tokenizer(LANGUAGE))
#parser = PlaintextParser.from_file("1.txt", Tokenizer(LANGUAGE))

stemmer = Stemmer(LANGUAGE)
summarizer = LsaSummarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)

# выводим резюме
for sentence in summarizer(parser.document, SENTENCES_COUNT):
	print(sentence)




# Асинхронность - это способ выполнения задач, при котором они могут быть запущены одновременно и выполняться независимо друг от друга. Она позволяет программе продолжать работать, не ожидая завершения каждой задачи. Это особенно полезно при работе с долгими или ресурсоемкими операциями, такими как загрузка данных из Интернета или выполнение сложных вычислений, позволяя приложению оставаться отзывчивым и эффективным.

# Это особенно полезно при работе с долгими или ресурсоемкими операциями, такими как загрузка данных из Интернета или выполнение сложных вычислений, позволяя приложению оставаться отзывчивым и эффективным.



# from transformers import pipeline

# summarizer = pipeline("summarization")

# text = " Gensim: Он имеет функции для суммаризации текста. Он использует алгоритмы, основанные на фразах и рангах, чтобы уплотнить текст, сохраняя при этом его смысл."

# # Его суммаризация
# summarizer(text, max_length=130, min_length=30, do_sample=False)
























# from keys import api_key

# from openai import AsyncOpenAI
# import asyncio



# client = AsyncOpenAI(
#     api_key=api_key,
# )


# async def main():
#     stream = await client.chat.completions.create(
#         model="gpt-4",
#         messages=[{"role": "user", "content": "Say this is a test"}],
#         stream=True,
#     )
#     async for chunk in stream:
#         print(chunk.choices[0].delta.content or "", end="")


# asyncio.run(main())





#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
# from sqlalchemy.orm import relationship, sessionmaker
# from models import UsersTelegram, engine



# Session = sessionmaker(bind=engine)
# session = Session()

# users = session.query(UsersTelegram).all()
# for user in users:
#     print(f'User: {user.user_id}, Email: {user.user_username}, id: {user.id}')







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