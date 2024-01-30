from sqlalchemy.orm import relationship, sessionmaker
from models import UsersTelegram, ChatGpt, SavedQuestion, engine

# Conection DB
Session = sessionmaker(bind=engine) # Создаем сессию для работы с базой данных
session = Session()

# Reading all data telegram by user ID
def read_tele_user(id):
    user_data = session.query(UsersTelegram).filter(UsersTelegram.id == id).all()
    for data in user_data:
        return data.id, data.user_username, data.user_first_name, data.user_last_name, data.chat_id or None
    
# Writing or Update all telegram data user, abstractness
def add_update_tele_user(id, user_username=None, user_first_name=None, user_last_name=None, chat_id=None, is_user_admin=None, is_user_block=None, is_user_good=None):
    existing_data = session.query(UsersTelegram).filter_by(id=id).first()
    
    if existing_data:
        if id is not None:
            existing_data.id = id
        if user_username is not None:
            existing_data.user_username = user_username
        if user_first_name is not None:
            existing_data.user_first_name = user_first_name
        if user_last_name is not None:
            existing_data.user_last_name = user_last_name
        if chat_id is not None:
            existing_data.chat_id = chat_id
        if is_user_admin is not None:
            existing_data.is_user_admin = is_user_admin
        if is_user_block is not None:
            existing_data.is_user_block = is_user_block
        if is_user_good is not None:
            existing_data.is_user_good = is_user_good
    else:
        new_user = UsersTelegram()

        if id is not None:
            new_user.id = id
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

    existing_settings = session.query(ChatGpt).filter_by(id=id).first()
    if existing_settings is None:
        new_chatgpt_settings = ChatGpt(id=id)
        session.add(new_chatgpt_settings)
        session.commit()
        
    existing_saved_question = session.query(SavedQuestion).filter_by(users_telegram_id=id).first()
    if existing_saved_question is None:
        new_saved_question = SavedQuestion(users_telegram_id=id)
        session.add(new_saved_question)
        session.commit()

# Read all settings ChatGpt in Base
def get_settings(id):
    read_data = session.query(ChatGpt).filter(ChatGpt.id == id).all()
    for data in read_data:
        return data.id, data.temp_chat, data.lang_chat, data.count_req_chat, data.used_token_chat, data.limit_token_chat, data.the_gap, data.model_id or None

# Write or Update settings ChatGpt in Base, abstractness  -   update_settings(id, temp_chat=temp, lang_chat=lang, count_req_chat=count, used_token_chat=all_token, limit_token_chat=limit_token, the_gap=the_gap, model_id=model_chat) # Вносим изменения в настройки
def add_update_settings(id, temp_chat=None, lang_chat=None, count_req_chat=None, used_token_chat=None, limit_token_chat=None, the_gap=None, model_id=None):
    
    existing_data = session.query(ChatGpt).filter_by(id=id).first() # Ищем запись по id

    if existing_data:
        if temp_chat is not None:
            existing_data.temp_chat = temp_chat
        if lang_chat is not None:
            existing_data.lang_chat = lang_chat
        if count_req_chat is not None:
            existing_data.count_req_chat = count_req_chat
        if used_token_chat is not None:
            existing_data.used_token_chat = used_token_chat
        if limit_token_chat is not None:
            existing_data.limit_token_chat = limit_token_chat
        if the_gap is not None:
            existing_data.the_gap = the_gap
        if model_id is not None:
            existing_data.model_id = model_id
    else:
        new_user = ChatGpt()

        if temp_chat is not None:
            new_user.temp_chat = temp_chat
        if lang_chat is not None:
            new_user.lang_chat = lang_chat
        if count_req_chat is not None:
            new_user.count_req_chat = count_req_chat
        if used_token_chat is not None:
            new_user.used_token_chat = used_token_chat
        if limit_token_chat is not None:
            new_user.limit_token_chat = limit_token_chat
        if the_gap is not None:
            new_user.the_gap = the_gap
        if model_id is not None:
            new_user.model_id = model_id
        session.add(new_user)

    session.commit()

# Read all data history Answer-Question in the Base
def read_history_db(id):
    read_data = session.query(SavedQuestion).filter(SavedQuestion.users_telegram_id == id).all()
    for data in read_data:
        return data.question_text, data.timestamp or None

# Writing Answer-Question to the Base
def update_talking(id, session_data):
    existing_data = session.query(SavedQuestion).filter_by(users_telegram_id=id).first() # Ищем запись по id

    if existing_data:
        existing_data.question_text = session_data # Если запись существует, обновляем значение столбца question_text
    else:
        new_data = SavedQuestion(users_telegram_id=id, question_text=session_data) # Если запись не существует, создаем новую запись
        session.add(new_data)

    session.commit()# Сохраняем изменения в базе данных
