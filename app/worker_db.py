from sqlalchemy.orm import relationship, sessionmaker
from models import UsersTelegram, ChatGpt, SavedQuestion, engine


# Conection DB
Session = sessionmaker(bind=engine) # Создаем сессию для работы с базой данных
session = Session()


# Reading User telegram data
def read_tele_user(user_id):
    user_data = session.query(UsersTelegram).filter(UsersTelegram.user_id == user_id).all()
    for data in user_data:
        return data.user_id, data.user_username, data.user_first_name, data.user_last_name, data.id 
        # if data.id: 
        #     return data.user_id, data.user_username, data.user_first_name, data.user_last_name, data.id 
        # else:
        #     print("Error: Dont have user to this id !!!")
        #     return None


##### Позже объеденить #####
    
# Writing User telegram data
def add_tele_user(user_id, user_username, user_first_name, user_last_name):
    new_user = UsersTelegram(user_id=user_id, user_username=user_username, user_first_name=user_first_name, user_last_name=user_last_name)
    session.add(new_user)
    session.commit()

# Writing Default id Setings ChatGpt
def add_chatgpt_setings(id):
    new_user = ChatGpt(id=id)
    session.add(new_user)
    session.commit()

# Writing Default id SavedQuestion
def add_new_session_data(id):
    new_user = SavedQuestion(users_telegram_id=id)
    session.add(new_user)
    session.commit()

##### Позже объеденить #####



# Read Setings ChatGpt to the Base
def read_chatgpt_setings(id):
    pass

# Writing Answer-Question to the Base
def add_session_data(user_id, session_data):
    # Пытаемся найти существующую запись для указанного user_id
    existing_data = session.query(SavedQuestion).filter_by(users_telegram_id=user_id).first()

    if existing_data:
        # Если запись существует, обновляем значение столбца question_text
        existing_data.question_text = session_data
    else:
        # Если запись не существует, создаем новую запись
        new_data = SavedQuestion(users_telegram_id=user_id, question_text=session_data)
        session.add(new_data)

    # Сохраняем изменения в базе данных
    session.commit()





    # data = SavedQuestion(question_text=session_data)
    # session.add(data)
    # session.commit()

# Read Answer-Question to the Base
def read_session_data(user_id, ):
    pass
    timestamp = 1
    return timestamp