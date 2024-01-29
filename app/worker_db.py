from sqlalchemy.orm import relationship, sessionmaker
from models import UsersTelegram, ChatGpt, SavedQuestion, engine


# Conection DB
Session = sessionmaker(bind=engine) # Создаем сессию для работы с базой данных
session = Session()


# Reading all data telegram by user ID
def read_tele_user(id):
    user_data = session.query(UsersTelegram).filter(UsersTelegram.id == id).all()
    for data in user_data:
        return data.id, data.user_username, data.user_first_name, data.user_last_name, data.chat_id
    
# Writing all telegram data user, abstractness
def add_tele_user(user_id=None, user_username=None, user_first_name=None, user_last_name=None, chat_id=None, is_user_admin=None, is_user_block=None, is_user_good=None):
    new_user = UsersTelegram()

    if user_id is not None:
        new_user.id = user_id
    if user_username is not None:
        new_user.user_username = user_username
    if user_first_name is not None:
        new_user.user_first_name = user_first_name
    if user_last_name is not None:
        new_user.user_last_name = user_last_name
    if chat_id is not None:
        new_user.chat_id = chat_id
    if is_user_admin is not None:
        new_user.is_user_admin = is_user_admin
    if is_user_block is not None:
        new_user.is_user_block = is_user_block
    if is_user_good is not None:
        new_user.is_user_good = is_user_good
 
    session.add(new_user)
    session.commit()

# Set default settings when add new user
def add_default_data(id):
    new_chatgpt_settings = ChatGpt(id=id)
    session.add(new_chatgpt_settings)
    new_saved_question = SavedQuestion(users_telegram_id=id)
    session.add(new_saved_question)
    session.commit()

# # Writing Default id Setings ChatGpt
# def add_chatgpt_setings(id):
#     new_user = ChatGpt(id=id)
#     session.add(new_user)
#     session.commit()

# # Writing Default id SavedQuestion
# def add_new_session_data(id):
#     new_user = SavedQuestion(users_telegram_id=id)
#     session.add(new_user)
#     session.commit()




# Read Answer-Question in the Base
def read_data_ans_ques(id):
    read_data = session.query(SavedQuestion).filter(SavedQuestion.users_telegram_id == id).all()
    for data in read_data:
        return data.question_text, data.timestamp or None


# Writing Answer-Question to the Base
def add_session_data(user_id, session_data):
    existing_data = session.query(SavedQuestion).filter_by(users_telegram_id=user_id).first() # Ищем запись по id

    if existing_data:
        existing_data.question_text = session_data # Если запись существует, обновляем значение столбца question_text
    else:
        new_data = SavedQuestion(users_telegram_id=user_id, question_text=session_data) # Если запись не существует, создаем новую запись
        session.add(new_data)

    session.commit()# Сохраняем изменения в базе данных


# Read settings ChatGpt in Base
def get_settings(id):
    read_data = session.query(ChatGpt).filter(ChatGpt.id == id).all()
    for data in read_data:
        return data.id, data.temp_chat, data.lang_chat, data.count_req_chat, data.used_token_chat, data.limit_token_chat, data.the_gap, data.model_id or None

# Write settings ChatGpt in Base
def update_settings(id, all_token, limit_token):
    existing_data = session.query(ChatGpt).filter_by(id=id).first() # Ищем запись по id
    existing_data.used_token_chat = all_token
    existing_data.limit_token_chat = limit_token
    session.commit()
    # read_data = session.query(ChatGpt).filter(ChatGpt.id == id).all()
    # for data in read_data:
    #     return data.id, data.temp_chat, data.lang_chat, data.count_req_chat, data.used_token_chat, data.limit_token_chat, data.the_gap, data.model_id or None

    # data = SavedQuestion(question_text=session_data)
    # session.add(data)
    # session.commit()

# Read Answer-Question to the Base
# def read_session_data(user_id, ):
#     pass
#     timestamp = 1
#     return timestamp