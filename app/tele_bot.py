import telebot
from keys import token
from worker_db import read_tele_user, add_tele_user, add_chatgpt_setings


bot = telebot.TeleBot(token) # Conection for API Telegram




# /start
@bot.message_handler(commands=['start'])
def start(context):
    # Проверяем где есть имя у Телегарм польз-ля
    if context.from_user.username:
        about = context.from_user.username
    elif context.from_user.first_name:
        about = context.from_user.first_name
    elif context.from_user.last_name:
        about = context.from_user.last_name
    else:
        about = "друг"
    # Выводим привествие пользователю
    bot.send_message(context.chat.id, text=f"Привет, {about}! Я ChatGPT бот.\nМне можно сразу задать вопрос\nили настроить - /setup.")
    user_id = context.from_user.id # Телеграм id нажавшего старт
    read_id = read_tele_user(user_id) # Считываем в базе с таким id все его данные
    # user_id_1, user_username_1, user_db_id_1 = read_id # Теперь вы можете извлечь значения из кортежа
    # print(user_id_1)
    # Если в базе нет такого id то добавляем
    if read_id == None:
        add_tele_user(context.from_user.id, context.from_user.username, context.from_user.first_name, context.from_user.last_name)
        # Вычитываю из таблицы UserTelegram только что добавленного пользователя, а конкретно id следуюет 4ым в кортеже
        added_user_id = read_tele_user(user_id)[4] # Получили id только что внесенного пользователя
        # Вносим id в таблицу настроек gpt, нужное проставиться по default
        add_chatgpt_setings(added_user_id)




    # user_id = context.from_user.id
    # user_first_name = context.from_user.first_name  # Имя пользователя
    # user_last_name = context.from_user.last_name  # Фамилия пользователя (может быть None)
    # user_username = context.from_user.username  # Юзернейм пользователя (может быть None)
    # chat_id = context.chat.id



start_bot = bot.polling()
