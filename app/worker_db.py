from sqlalchemy.orm import relationship, sessionmaker
from models import UsersTelegram, ChatGpt, SavedQuestion, Statistic, Exchange, engine

# Conection DB
Session = sessionmaker(bind=engine) # Создаем сессию для работы с базой данных
session = Session()


# READ AND WRITING DATA TO TABLES
# Reading user data telegram by user ID
def read_tele_user(id):
    data = session.query(UsersTelegram)\
        .filter(UsersTelegram.id == id)\
            .first()
    if data:
        return  data.id, data.user_username, data.user_first_name,\
                data.user_last_name, data.chat_id, data.is_user_admin,\
                data.is_user_block, data.is_user_good or None
    else:
        return None, None

# Writing or Update all telegram data user, abstractness
def add_update_tele_user(id, user_username=None, user_first_name=None, user_last_name=None,\
                          chat_id=None, is_user_admin=None, is_user_block=None, is_user_good=None):
    existing_data = session.query(UsersTelegram)\
        .filter_by(id=id)\
            .first()
    
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

    existing_settings = session.query(ChatGpt)\
        .filter_by(id=id)\
            .first()
    if existing_settings is None:
        new_chatgpt_settings = ChatGpt(id=id)
        session.add(new_chatgpt_settings)
        session.commit()
        
    existing_saved_question = session.query(SavedQuestion)\
        .filter_by(users_telegram_id=id)\
            .first()
    if existing_saved_question is None:
        new_saved_question = SavedQuestion(users_telegram_id=id)
        session.add(new_saved_question)
        session.commit()

# Read user settings ChatGpt in Base
def get_settings(id):
    read_data = session.query(ChatGpt)\
        .filter(ChatGpt.id == id)\
            .first()
    if read_data:
        return  read_data.id, read_data.temp_chat, read_data.lang_chat, read_data.count_req_chat,\
                read_data.used_token_chat, read_data.limit_token_chat, read_data.the_gap, read_data.model_id,\
                read_data.money_user, read_data.total_spent_money or None
    else:
        return None, None

# Write or Update settings ChatGpt in Base, abstractness  # Вносим изменения в настройки
def add_update_settings(id, temp_chat=None, lang_chat=None, count_req_chat=None, used_token_chat=None,\
                        limit_token_chat=None, the_gap=None, model_id=None, money_user=None,\
                        total_spent_money=None):
    
    existing_data = session.query(ChatGpt)\
        .filter_by(id=id)\
            .first() # Ищем запись по id

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
        if money_user is not None:
            existing_data.money_user = money_user
        if total_spent_money is not None:
            existing_data.total_spent_money = total_spent_money
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
        if money_user is not None:
            new_user.money_user = money_user
        if total_spent_money is not None:
            new_user.total_spent_money = total_spent_money

        session.add(new_user)

    session.commit()

# Read user data history Answer-Question in the Base
def read_history_db(id):
    read_data = session.query(SavedQuestion)\
        .filter(SavedQuestion.users_telegram_id == id)\
            .first()
    if read_data:
        return read_data.question_text, read_data.timestamp or None
    else:
        return None, None

# Writing Answer-Question to the Base
def update_talking(id, session_data):
    existing_data = session.query(SavedQuestion)\
        .filter_by(users_telegram_id=id)\
            .first()

    if existing_data:
        existing_data.question_text = session_data # Если запись существует, обновляем значение столбца question_text
    else:
        new_data = SavedQuestion(users_telegram_id=id, question_text=session_data) # Если запись не существует, создаем новую запись
        session.add(new_data)

    session.commit()# Сохраняем изменения в базе данных



# Exchgange

# Read price exchange USD to RUB
def get_exchange():
    data = session.query(Exchange)\
            .first() # Ищем любую запись, она там одна
    if data:
        return data.timestamp, data.price or None
    else:
        return None, None
    

# Write new price exchange USD to DB
def write_exchange(timestamp=None, price=None):
    data = session.query(Exchange)\
            .first() # Ищем любую запись
    if data:
        if timestamp is not None:
            data.timestamp = timestamp
        if price is not None:
            data.price = price
    else:
        new = Exchange()
        if timestamp is not None:
            new.timestamp = timestamp
        if price is not None:
            new.price = price
        session.add(new)
    session.commit()


#STATISTIC

# Read all statistic data 
def read_stat_db(id):
    data = session.query(Statistic)\
        .filter(Statistic.users_telegram_id == id)\
            .first()
    if data:
        return  data.id, data.time, data.model,\
                data.used_token, data.cost_token,\
                data.entire_cost, data.users_telegram_id or None
    else:
        return None, None
 

# Writing statistic data by user
def write_stat_db(model=None, used_token=None, cost_token=None, entire_cost=None, users_telegram_id=None):
    new = Statistic()

    if model is not None:
        new.model = model
    if used_token is not None:
        new.used_token = used_token
    if cost_token is not None:
        new.cost_token = cost_token
    if entire_cost is not None:
        new.entire_cost = entire_cost
    if users_telegram_id is not None:
        new.users_telegram_id = users_telegram_id

    session.add(new)
    session.commit()


# Get all Statistic to Admin
def admin_static_db():
    all_data = session.query(UsersTelegram, ChatGpt)\
        .filter(UsersTelegram.id == ChatGpt.id)\
            .all()
    user_data_list = []
    for user, chat_gpt in all_data:
        user_data_list.append((user.user_username, user.user_first_name,\
                                chat_gpt.used_token_chat, chat_gpt.limit_token_chat))
    return user_data_list
