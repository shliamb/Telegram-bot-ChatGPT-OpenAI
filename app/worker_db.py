from sqlalchemy.orm import relationship, sessionmaker
from models import UsersTelegram, engine


# Conection DB
Session = sessionmaker(bind=engine)
session = Session()


# Reading User Telegram in a Base
def read_tele_user(absd):
    users = session.query(UsersTelegram).filter(UsersTelegram.user_id == absd).all()
    for user in users:
        #print(f'User: {user.user_id}, Email: {user.user_username}, id: {user.id}')
        return user.user_id, user.user_username, user.id

# Writing User Telegram to the Base
def add_tele_user(user_id, user_username):
    new_user = UsersTelegram(user_id=user_id, user_username=user_username)
    session.add(new_user)
    session.commit()