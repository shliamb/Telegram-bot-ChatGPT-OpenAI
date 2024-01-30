import telebot
from telebot import types
from keys import token, azil, asilisav, admin_user_ids, block
from worker_db import read_tele_user, add_update_tele_user, add_default_data, get_settings, update_talking, add_update_settings
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
        about = "bro"

    bot.send_message(context.chat.id, text=f"Привет {about}! Мне можно сразу задать вопрос или сначала настроить - /setup.")
    # If this user is not in the database, we will add or update
    add_update_tele_user(id=id, user_username=name, user_first_name=first_name, user_last_name=last_name, chat_id=chat, is_user_admin=is_user_admin , is_user_block=is_user_block , is_user_good=is_user_good) # abstractness
    add_default_data(id) # Set default settings and text


# # /admin - статистика будет, загруженность базы, токены..
# @bot.message_handler(commands=['admin'])
# def start(context): 


# Messages to OpenAI
@bot.message_handler(func=lambda message: message.text is not None and not message.text.startswith('/')) # Декоратор Telebot принимает все, кроме того, что начинается на /
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing') # Typing bot
    id = message.from_user.id # Telegram id user were send message
    read_user_all_data = read_tele_user(id) # Reading in DB all data for user id
    if read_user_all_data == None:
        start(message) # If the user has not clicked / start, click it now
        print(f"Error: This User ID is None in DB. Automatically add.")

    async def run_main():
        bot.send_chat_action(message.chat.id, 'typing') # Typing bot
        result = await main(message.text, id) # Send to open_ai.py
        send = f"{result[0]}\n\nМодель: {result[1]}\nТокенов: {result[2]}\nНастроить: /setup"#\nЛимит токенов: {result[3]}"
        bot.reply_to(message, send) # Send to Telegram user 
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)       #  гавно какое то, нужно разобраться..
    loop.run_until_complete(run_main())


# Menu /setup or /menu
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

# Submenu Model
def model(call):
    keyboard = types.InlineKeyboardMarkup(row_width=1) # 3
    gpt4 = types.InlineKeyboardButton(text="ChatGPT 4", callback_data="gpt4")
    gpt4_1 = types.InlineKeyboardButton(text="ChatGPT 4 1106 preview", callback_data="gpt4_1")
    gpt3_5 = types.InlineKeyboardButton(text="ChatGPT 3.5 turbo", callback_data="gpt3_5")
    keyboard.add(gpt4, gpt4_1, gpt3_5)
    back_button = types.InlineKeyboardButton(text="Назад в главное меню", callback_data="back_menu")
    keyboard.row(back_button)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите модель ChatGPT:", reply_markup=keyboard)

# Submenu Time Limit
def time_limit(call):
    #settings = get_settings(id) # Get in DB all data settings
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    min30 = types.InlineKeyboardButton(text="30 мин", callback_data="min30")
    min15 = types.InlineKeyboardButton(text="15 мин", callback_data="min15")
    min5 = types.InlineKeyboardButton(text="5 мин", callback_data="min5")
    min0 = types.InlineKeyboardButton(text="Не запоминать", callback_data="min0")
    keyboard.add(min30, min15, min5, min0)
    back_button = types.InlineKeyboardButton(text="Назад в главное меню", callback_data="back_menu")
    keyboard.row(back_button)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите время ChatGPT:", reply_markup=keyboard)

# # SubMenu Reset dialog
def reset(call):
    id = call.from_user.id # telegram id user
    update_talking(id, session_data='')
    bot.answer_callback_query(call.id, text='Ваш диалог с ChatGPT сброшен 😉', show_alert=True)

# SubMenu Statistic
def stat(call):
    id = call.from_user.id # telegram id user
    settings = get_settings(id) # Get in DB all data settings
    model_chat = settings[7] # Модель
    the_gap = settings[6] # Часы.минуты время использования истории общения
    total_used_token = settings[4] # Всего использованно токенов
    limit_token = settings[5] # Выданный лимит токенов
    bot.answer_callback_query(call.id, text=f"Версия модели: {model_chat}\nВремя хранения диалога: {the_gap}\nВсего использованно токенов: {total_used_token}\nЛимит токенов: {limit_token}", show_alert=True)

# Закрыть клавиатуру
@bot.callback_query_handler(func=lambda call: call.data == "close_menu")
def handle_close_menu(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

# Работа Меню
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id if call.message is not None else None
    id = call.from_user.id # telegram id user
    # Model
    if call.data == "model":
        model(call)
    elif call.data == "gpt4":
        model_id="gpt-4"
        add_update_settings(id, model_id=model_id)
        bot.answer_callback_query(call.id, "Вы выбрали ChatGPT 4!")
    elif call.data == "gpt4_1":
        model_id="gpt-4-1106-preview"
        add_update_settings(id, model_id=model_id)
        bot.answer_callback_query(call.id, "Вы выбрали ChatGPT 4 1106 preview!")
    elif call.data == "gpt3_5":
        model_id="gpt-3.5-turbo"
        add_update_settings(id, model_id=model_id)
        bot.answer_callback_query(call.id, "Вы выбрали ChatGPT 3.5 turbo!")
    # Time
    elif call.data == "time_limit":
        time_limit(call)
    elif call.data == "min30":
        the_gap = 0.3
        add_update_settings(id, the_gap=the_gap)
        bot.answer_callback_query(call.id, "ChatGPT будет помнить диалог 30 минут!")
    elif call.data == "min15":
        the_gap = 0.15
        add_update_settings(id, the_gap=the_gap)
        bot.answer_callback_query(call.id, "ChatGPT будет помнить диалог 15 минут!")
    elif call.data == "min5":
        the_gap = 0.05
        add_update_settings(id, the_gap=the_gap)
        bot.answer_callback_query(call.id, "ChatGPT будет помнить диалог 5 минут!")
    elif call.data == "min0":
        the_gap = 0
        add_update_settings(id, the_gap=the_gap)
        bot.answer_callback_query(call.id, "ChatGPT не будет помнить диалог!")
    # Reset
    elif call.data == "reset":
        reset(call)
    # Statistic
    elif call.data == "stat":
        stat(call)
    # Menu Back
    elif call.data == "back_menu":
        pass
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



