import telebot
from telebot import types
from keys import token, white_list, admin_user_ids, block
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
    
    # If this user is not in the database, we will add or update
    add_update_tele_user(id=id, user_username=name, user_first_name=first_name, user_last_name=last_name, chat_id=chat, is_user_admin=is_user_admin , is_user_block=is_user_block , is_user_good=is_user_good) # abstractness
    add_default_data(id) # Set default settings and text
    
    # Checking and added the parameters in Settings to white list users
    if str(id) in white_list:
        limit = 1000000000
        add_update_settings(id, limit_token_chat=limit)
    
    # Choosing a name user
    if name:
        about = name
    elif first_name:
        about = first_name
    elif last_name:
        about = last_name
    else:
        about = "bro"

    bot.send_message(context.chat.id, text=f"Привет {about}! Мне можно сразу задать вопрос или сначала настроить - /setup.")


# /admin - статистика будет, загруженность базы, токены..
@bot.message_handler(commands=['admin'])
def admin(call):
    id = call.from_user.id # telegram id user
    data = read_tele_user(id)
    if data: # ебанная параноя..
        if data[5] == True:
            bot.send_message(call.chat.id, text=f"Статистика для админа Админ")
        else:
            bot.send_message(call.chat.id, text=f"Извините, вас нет в списках администраторов.")
            #bot.answer_callback_query(call.id, "ChatGPT будет помнить диалог 5 минут!") - не пашет

# Messages to OpenAI
@bot.message_handler(func=lambda message: message.text is not None and not message.text.startswith('/')) # Декоратор Telebot принимает все, кроме того, что начинается на /
def handle_message(message):
    id = message.from_user.id # telegram id user
    user_limit_tokens = get_settings(id)
    if user_limit_tokens:
        if user_limit_tokens[5] > 0 and user_limit_tokens[5] != 0:
            #raise
            bot.send_chat_action(message.chat.id, 'typing') # Typing bot
            read_user_all_data = read_tele_user(id) # Reading in DB all data for user id
            if read_user_all_data == None:
                start(message) # If the user has not clicked / start, click it now
                print(f"Error: This User ID is None in DB. Automatically add.")

            async def run_main():
                bot.send_chat_action(message.chat.id, 'typing') # Typing bot
                result = await main(message.text, id) # Send to open_ai.py
                send = f"{result[0]}\n\n\nМодель: {result[1]}\nТокенов: {result[2]}\nНастроить: /setup"#\nЛимит токенов: {result[3]}"
                bot.reply_to(message, send) # Send to Telegram user 
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)       #  гавно какое то, нужно разобраться..
            loop.run_until_complete(run_main())
        else:
            bot.send_message(message.chat.id, text=f"Извините, но похоже, у вас закончились токены.\n@Shliambur") # bot.answer_callback_query(message.id, text='Вы заблокированы! Попробуйте выключить телефон. 😉', show_alert=True)


# Menu Telebot
# Close mian menu
@bot.callback_query_handler(func=lambda call: call.data == "close_menu")
def handle_close_menu(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

# Menu /setup or /menu
@bot.message_handler(commands=['setup', 'menu', 'setings', 'set'])
def main_menu(message):
    #id = message.from_user.id # telegram id user
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    model = types.InlineKeyboardButton(text="Модель ChatGPT", callback_data="model")
    time_limit = types.InlineKeyboardButton(text="Сколько помнить диалог", callback_data="time_limit")
    reset = types.InlineKeyboardButton(text="Сбросить диалог", callback_data="reset")
    stat = types.InlineKeyboardButton(text="Статистика", callback_data="stat")
    close_menu_button = types.InlineKeyboardButton(text="Закрыть меню ✖️", callback_data="close_menu")
    keyboard.add(model, time_limit, reset, stat, close_menu_button)
    bot.send_message(message.chat.id, "Настройки ChatGPT:", reply_markup=keyboard)

# Submenu at Main Menu - Model
def model(call):
    keyboard = types.InlineKeyboardMarkup(row_width=1) # 3
    gpt4_1 = types.InlineKeyboardButton(text="ChatGPT 4 1106 Turbo", callback_data="gpt4_1")
    gpt4 = types.InlineKeyboardButton(text="ChatGPT 4 0613", callback_data="gpt4")
    gpt3_5 = types.InlineKeyboardButton(text="ChatGPT 3.5 Turbo", callback_data="gpt3_5")
    keyboard.add(gpt4_1, gpt4, gpt3_5)
    back_button = types.InlineKeyboardButton(text="🔙 Назад в главное меню", callback_data="back_menu")
    keyboard.row(back_button)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите модель ChatGPT:", reply_markup=keyboard)

# Back in Submenu Model to Main Menu
def back_menu(call):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    model = types.InlineKeyboardButton(text="Модель ChatGPT", callback_data="model")
    time_limit = types.InlineKeyboardButton(text="Сколько помнить диалог", callback_data="time_limit")
    reset = types.InlineKeyboardButton(text="Сбросить диалог", callback_data="reset")
    stat = types.InlineKeyboardButton(text="Статистика", callback_data="stat")
    close_menu_button = types.InlineKeyboardButton(text="Закрыть меню ✖️", callback_data="close_menu")
    keyboard.add(model, time_limit, reset, stat, close_menu_button)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Настройки ChatGPT:", reply_markup=keyboard)

# Submenu at Main Menu - Time Limit
def time_limit(call):
    #settings = get_settings(id) # Get in DB all data settings
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    min30 = types.InlineKeyboardButton(text="30 мин", callback_data="min30")
    min15 = types.InlineKeyboardButton(text="15 мин", callback_data="min15")
    min5 = types.InlineKeyboardButton(text="5 мин", callback_data="min5")
    min0 = types.InlineKeyboardButton(text="Не запоминать", callback_data="min0")
    keyboard.add(min30, min15, min5, min0)
    back_button = types.InlineKeyboardButton(text="🔙 Назад в главное меню", callback_data="back_menu")
    keyboard.row(back_button)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите время ChatGPT:", reply_markup=keyboard)

# # SubMenu at Main Menu - Reset dialog
def reset(call):
    id = call.from_user.id # telegram id user
    update_talking(id, session_data='')
    bot.answer_callback_query(call.id, text='Ваш диалог с ChatGPT сброшен 😉', show_alert=True)

# SubMenu at Main Menu - Statistic
def stat(call):
    id = call.from_user.id # telegram id user
    settings = get_settings(id) # Get in DB all data settings
    if settings is not None:
        model_chat = settings[7] # Модель
        the_gap = settings[6] # Часы.минуты время использования истории общения
        total_used_token = settings[4] # Всего использованно токенов
        limit_token = settings[5] # Выданный лимит токенов
        bot.answer_callback_query(call.id, text=f"Версия модели: {model_chat}\nВремя хранения диалога: {the_gap} час.\nВсего использованно токенов: {total_used_token}\nЛимит токенов: {limit_token}", show_alert=True)

# Script worcking Menu
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
        back_menu(call)





# будет какой то модуль оплаты
# Туда можно будет поместить заблокированных, что бы не могли оплатить, ну мало ли..
# Не может оплатить - не может пользоваться..  
# id = message.from_user.id # telegram id user
# is_user_blocked = read_tele_user(id)
# if is_user_blocked:
#     if is_user_blocked[6] == False:
#         pass
#     else:
#         bot.send_message(message.chat.id, text=f"Извините, но похоже, что вы заблокированы! 😉\nПопробуйте связаться с @Shliambur") # bot.answer_callback_query(message.id, text='Вы заблокированы! Попробуйте выключить телефон. 😉', show_alert=True)






#####
start_bot = bot.polling() # Запуск инициализируется в run_bot.py