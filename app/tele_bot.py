import telebot
from telebot import types
from keys import token, azil, asilisav, admin_user_ids
from worker_db import read_tele_user, add_tele_user, add_chatgpt_setings, add_new_session_data
import asyncio
from open_ai import main

bot = telebot.TeleBot(token) # Conection for API Telegram

# /start
@bot.message_handler(commands=['start'])
def start(context):
    #print(admin_user_ids)
    #print(context.from_user.id)
    # Проверяем где есть имя у Телегарм польз-ля
    if int(context.from_user.id) == int(azil) or int(context.from_user.id) == int(asilisav):
        about = "доченька от папы"
    if int(context.from_user.id) == int(admin_user_ids):
        about = "брооооо"
    elif context.from_user.username:
        about = context.from_user.username
    elif context.from_user.first_name:
        about = context.from_user.first_name
    elif context.from_user.last_name:
        about = context.from_user.last_name
    else:
        about = "друг"
    # Выводим привествие пользователю
    bot.send_message(context.chat.id, text=f"Привет {about}! Мне можно сразу задать вопрос или сначала настроить - /setup.")
    user_id = context.from_user.id # Телеграм id нажавшего старт
    read_id = read_tele_user(user_id) # Считываем в базе с таким id все его данные
    # user_id_1, user_username_1, user_db_id_1 = read_id # Теперь вы можете извлечь значения из кортежа
    # print(user_id_1)
    # Если в базе нет такого id то добавляем
    if read_id == None:
        add_tele_user(context.from_user.id, context.from_user.username, context.from_user.first_name, context.from_user.last_name)
        ##### Позже объеденить я могу получить user_id прямо там и там же подставить ##### 
        # Вычитываю из таблицы UserTelegram только что добавленного пользователя, а конкретно id следуюет 4ым в кортеже
        added_user_id = read_tele_user(user_id)[4] # Получили id только что внесенного пользователя
        add_chatgpt_setings(added_user_id) # Вносим id в таблицу настроек gpt, нужное проставиться по default
        add_new_session_data(added_user_id) # Вносим id в таблицу SavedQuestion, нужное проставиться по default
        ##### Позже объеденить я могу получить user_id прямо там и там же подставить ##### 

# # /admin - статистика будет, загруженность базы, токены..
# @bot.message_handler(commands=['admin'])
# def start(context): 


# Message from OpenAI
@bot.message_handler(func=lambda message: message.text is not None and not message.text.startswith('/')) # Декоратор Telebot принимает все, кроме того, что начинается на /
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing') # Typing bot

    user_id = message.from_user.id # Телеграм id начавшего диалог
    id_all = read_tele_user(user_id)# Вся строка по id в таблице Users Telegram
    if id_all == None:
        start(message) # Если почему то не нажал /start, нажимаем
        print("This User ID is None in DB. Automatically add.") # raise ValueError("ID is None. Program stopped. So Soory bro.") - жестко выйдет из программы
    id_all = read_tele_user(user_id)# Вся строка по id в таблице Users Telegram
    id = id_all[4] # id 4 по счету в кортеже

    async def run_main():
        bot.send_chat_action(message.chat.id, 'typing') # Typing bot
        result = await main(message.text, id)
        send = f"{result[0]}\n- - - - - - - - - - - - - - - - - - - - - - - - - -\nВерсия модели: {result[1]}\nТок. вопрос + ответ: {result[4]}\nТокенов за все время: {result[5]}\nТокенов осталось: {result[6]}" #Завершенные токены: {result[2]}\nПодсказки токены: {result[3]}\nВсего токенов: {result[4]}"
        # send = f"{переменная}\n<b>Жирным - b</b> <i>Курсив - i</i> <code>Код - code</code> <pre>Отдельный блок для копирования - pre</pre>"
        bot.reply_to(message, send) # bot.reply_to(message, send, parse_mode='HTML')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_main())


# Вызов меню /setup
# Главное меню
#flag_menu = False

@bot.message_handler(commands=['setup'])
def main_menu(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    version_chat = types.InlineKeyboardButton(text="Модель ChatGPT 🦾", callback_data="version_chat")
    version_dialog = types.InlineKeyboardButton(text="Время памяти 🗣", callback_data="mode_dialog")
    #version_creativity = types.InlineKeyboardButton(text="Уровень творчества 👻", callback_data="level_creativity")
    response_volume = types.InlineKeyboardButton(text="Статистика 👻", callback_data="response_volume")
    close_menu_button = types.InlineKeyboardButton(text="Закрыть меню ✖️", callback_data="close_menu")
    keyboard.add(version_chat, version_dialog, response_volume, close_menu_button)
    #if flag_menu == False:
    bot.send_message(message.chat.id, "Настройки ChatGPT:", reply_markup=keyboard)
        #flag_menu = True
    #else:
        #breakpoint
        #bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Выберите версию ChatGPT:", reply_markup=keyboard)


















#####
start_bot = bot.polling() # Запуск инициализируется в run_bot.py














    # user_id = context.from_user.id
    # user_first_name = context.from_user.first_name  # Имя пользователя
    # user_last_name = context.from_user.last_name  # Фамилия пользователя (может быть None)
    # user_username = context.from_user.username  # Юзернейм пользователя (может быть None)
    # chat_id = context.chat.id



