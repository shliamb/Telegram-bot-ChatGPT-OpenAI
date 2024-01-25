from sqlalchemy.orm import relationship, sessionmaker
from models import UsersTelegram, ChatGpt, engine


# Conection DB
Session = sessionmaker(bind=engine)
session = Session()


# Reading User Telegram in a Base
def read_tele_user(data):
    users = session.query(UsersTelegram).filter(UsersTelegram.user_id == data).all()
    for user in users:
        #print(f'User: {user.user_id}, Email: {user.user_username}, id: {user.id}')
        return user.user_id, user.user_username, user.user_first_name, user.user_last_name, user.id

# Writing User Telegram to the Base
def add_tele_user(user_id, user_username, user_first_name, user_last_name):
    new_user = UsersTelegram(user_id=user_id, user_username=user_username, user_first_name=user_first_name, user_last_name=user_last_name)
    session.add(new_user)
    session.commit()

# Writing Setings ChatGpt to the Base
def add_chatgpt_setings(id):
    new_user = ChatGpt(id=id)
    session.add(new_user)
    session.commit()