import telebot
from telebot import types
from keys import token, azil, asilisav, admin_user_ids, block
from worker_db import read_tele_user, add_tele_user, add_default_data, get_settings
import asyncio
from open_ai import main

bot = telebot.TeleBot(token) # Conection for API Telegram


# /start
@bot.message_handler(commands=['start'])
def start(context):
    id = context.from_user.id # telegram id user were tap /start
    name = context.from_user.username
    first_name = context.from_user.first_name
    last_name = context.from_user.last_name
    chat = context.chat.id
    is_user_admin = False
    is_user_block = False
    is_user_good = 3

    # Checking and added the parameters
    if str(id) in admin_user_ids:
        is_user_admin = True
    if str(id) in block:
        is_user_block=True
    # Choosing a name
    if int(id) == int(azil) or int(id) == int(asilisav):
        about = "доченька от папы"
        # Сделать лимиты бесконечные
    elif name:
        about = name
    elif first_name:
        about = first_name
    elif last_name:
        about = last_name
    else:
        about = "друг"

    bot.send_message(context.chat.id, text=f"Привет {about}! Мне можно сразу задать вопрос или сначала настроить - /setup.")
    read_user_all_data = read_tele_user(id) # Reading in DB all data for user id
    # If this user is not in the database, we will add
    if read_user_all_data == None:
        add_tele_user(user_id=id, user_username=name, user_first_name=first_name, user_last_name=last_name, chat_id=chat, is_user_admin=is_user_admin , is_user_block=is_user_block , is_user_good=is_user_good) # abstractness
        add_default_data(id)


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


# Вызов меню /setup or /menu
@bot.message_handler(commands=['setup', 'menu', 'setings', 'set'])
def main_menu(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    model = types.InlineKeyboardButton(text="Модель ChatGPT 🦾", callback_data="model")
    time_limit = types.InlineKeyboardButton(text="Сколько помнить диалог", callback_data="time_limit")
    reset = types.InlineKeyboardButton(text="Сбросить диалог 👻", callback_data="reset")
    stat = types.InlineKeyboardButton(text="Статистика 🗣", callback_data="stat")
    close_menu_button = types.InlineKeyboardButton(text="Закрыть меню ✖️", callback_data="close_menu")
    keyboard.add(model, time_limit, reset, stat, close_menu_button)
    bot.send_message(message.chat.id, "Настройки ChatGPT:", reply_markup=keyboard)
    #bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Выберите версию ChatGPT:", reply_markup=keyboard)

# Под меню mode_dialog
def model(call):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    amnesia = types.InlineKeyboardButton(text="Амнезия", callback_data="amnesia")
    dialog = types.InlineKeyboardButton(text="Диалог", callback_data="dialog")
    keyboard.add(amnesia, dialog)
    back_button = types.InlineKeyboardButton(text="Назад в главное меню", callback_data="back_menu")
    keyboard.row(back_button)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите режим ответа ChatGPT:", reply_markup=keyboard)

# Под меню time_limit
def time_limit(call):
    bot.answer_callback_query(call.id, "Вы нажали кнопку time_limit!")
    # keyboard = types.InlineKeyboardMarkup(row_width=2)
    # amnesia = types.InlineKeyboardButton(text="Амнезия", callback_data="amnesia")
    # dialog = types.InlineKeyboardButton(text="Диалог", callback_data="dialog")
    # keyboard.add(amnesia, dialog)
    # back_button = types.InlineKeyboardButton(text="Назад в главное меню", callback_data="back_menu")
    # keyboard.row(back_button)
    # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите режим ответа ChatGPT:", reply_markup=keyboard)

# Под меню reset
def reset(call):
    pass
    bot.answer_callback_query(call.id, text='Ваш диалог с ChatGPT сброшен 😉', show_alert=True)

# Под меню stat
def stat(call):
    bot.send_chat_action(call.chat.id, 'typing') # Typing bot
    # settings = get_settings(id)
    # model_chat = settings[7] # Модель
    # the_gap = settings[6] # Часы.минуты время использования истории общения
    # total_used_token = settings[4] # Всего использованно токенов
    # limit_token = settings[5] # Выданный лимит токенов
    # bot.answer_callback_query(call.id, text=f"Ваша статистика:\nВерсия модели: {model_chat}\nВремя хранения диалога: {the_gap}\nВсего использованно токенов: {total_used_token}\nЛимит токенов: {limit_token}", show_alert=True)

# Закрыть клавиатуру
@bot.callback_query_handler(func=lambda call: call.data == "close_menu")
def handle_close_menu(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

# Работа Меню
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id if call.message is not None else None

    if call.data == "model":
        model(call)
    elif call.data == "time_limit":
        #bot.answer_callback_query(call.id, "Вы нажали кнопку mode_dialog!")
        time_limit(call)
    elif call.data == "reset":
        reset(call)
    elif call.data == "stat":
        stat(call)
    elif call.data == "back_menu":
        if chat_id:
            main_menu(call.message)



















#####
start_bot = bot.polling() # Запуск инициализируется в run_bot.py









# bot.answer_callback_query(
#             callback_query.id,
#             text='Нажата кнопка с номером 5.\nА этот текст может быть длиной до 200 символов 😉', show_alert=True)




    # user_id = context.from_user.id
    # user_first_name = context.from_user.first_name  # Имя пользователя
    # user_last_name = context.from_user.last_name  # Фамилия пользователя (может быть None)
    # user_username = context.from_user.username  # Юзернейм пользователя (может быть None)
    # chat_id = context.chat.id



