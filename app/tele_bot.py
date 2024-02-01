import os
import telebot
from telebot import types
from keys import token, white_list, admin_user_ids, block
from worker_db import read_tele_user, add_update_tele_user, add_default_data, get_settings, update_talking, add_update_settings, admin_static_db
import asyncio
from open_ai import main
import csv
from io import StringIO, BytesIO
import datetime


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
    
    # If this user is not in the database, we will add or update, because the user could get a block
    add_update_tele_user(id=id, user_username=name, user_first_name=first_name, user_last_name=last_name, chat_id=chat, is_user_admin=is_user_admin , is_user_block=is_user_block , is_user_good=is_user_good) # abstractness
    add_default_data(id) # Set default settings and text
    
    # Checking and added the parameters in Settings to white list users And gives them money
    if str(id) in white_list:
        money = 1000
        add_update_settings(id, money_user=money) # Gives money
    
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


# Admin statistic lite menu /admin
@bot.message_handler(commands=['admin'])
def admin(call):
    id = call.from_user.id # telegram id user
    data = read_tele_user(id)
    if data: # ебанная параноя..
        if data[5] == True:
            bot.send_message(call.chat.id, text=f"Статистика: /admin_static\nСкачать: /log\nОчистить логи: /clearlog")
        else:
            bot.send_message(call.chat.id, text="Извините, вас нет в списках администраторов.")

# Admin statistic /admin_static
@bot.message_handler(commands=['admin_static'])
def admin_static(call):
    id = call.from_user.id # telegram id user
    bot.send_chat_action(call.chat.id, 'typing') # Typing bot
    data = read_tele_user(id)
    if data: # if the data exists
        if data[5] == True: # if user is admin
            static = admin_static_db()
            all_static = []
            all_static.append(["Name", "First name", "Used token", "Limit token"]) # First a names row
            for user_data in static:
                if all_static:
                    all_static.append([user_data[0], user_data[1], user_data[2], user_data[3]]) # added user data
            # Create CVS file
            output = StringIO()
            writer = csv.writer(output)
            for row in all_static:
                writer.writerow(row)
            csv_data = output.getvalue()
            output.close()
            # CVS file to download
            file = BytesIO(csv_data.encode())
            # Name file
            date_time = datetime.datetime.utcnow() # Current date and time
            formtime = date_time.strftime("%Y-%m-%d-%H-%M")
            
            file.name = f"Stat-{formtime}.csv"
            bot.send_document(call.chat.id, file)
        else:
            bot.send_message(call.chat.id, text="Извините, вас нет в списках администраторов.")

# Admin clear log /clearlog
@bot.message_handler(commands=['clearlog'])
def users_limits(call):
    id = call.from_user.id # telegram id user
    data = read_tele_user(id)
    if data:
        if data[5] == True:
            bot.send_chat_action(call.chat.id, 'typing') # Typing bot
            log_file_path = './log/app.log'
            # Send Server log file to bot
            with open(log_file_path, 'w'):
                pass
            bot.send_message(call.chat.id, text="Файл app.log очищен успешно.")
        else:
            bot.send_message(call.chat.id, text="Извините, вас нет в списках администраторов.")

# Admin downloud log file /log
@bot.message_handler(commands=['log'])
def log(call):
    id = call.from_user.id # telegram id user
    data = read_tele_user(id)
    if data:
        if data[5] == True:
            bot.send_chat_action(call.chat.id, 'typing') # Typing bot
            log_file_path = './log/app.log'
            # Send Server log file to bot
            if os.path.exists(log_file_path) and os.path.getsize(log_file_path) > 0: # Проверка на существование файла и его непустоту
                with open(log_file_path, 'rb') as log_file:
                    bot.send_document(call.chat.id, document=log_file)
            else:
                bot.send_message(call.chat.id, text="Файл логирования не найден или пустой.")
        else:
            bot.send_message(call.chat.id, text="Извините, вас нет в списках администраторов.")

# Messages to OpenAI
@bot.message_handler(func=lambda message: message.text is not None and not message.text.startswith('/')) # Декоратор Telebot принимает все, кроме того, что начинается на /
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing') # Typing bot
    id = message.from_user.id # telegram id user
    user_money = get_settings(id)
    if user_money != (None, None): # If no have data from user - created
        if user_money[8] > 0 and user_money[8] != 0:

            async def run_main():
                bot.send_chat_action(message.chat.id, 'typing') # Typing bot
                result = await main(message.text, id) # Send to open_ai.py
                # If result on 
                if result:
                    text = result[0] # Text response
                    model = result[1] # The name of the model geting from the OpenAI response
                    used_token = result[2]
                    money = result[3] # geting from the Calculation.py
                    # money = user_money[8]

                send = f"{text}\n\n\n{model}\nисп.:{used_token}токенов\nВсего:{money}руб.\nНастроить: /setup"
                bot.reply_to(message, send) # Send to Telegram user  - parse_mode='HTML'
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)       #  гавно какое то, нужно разобраться..
            loop.run_until_complete(run_main())

        else:
            bot.send_message(message.chat.id, text=f"Извините, но похоже, у вас нулевой баланс.\n Пополнить - /setup") # bot.answer_callback_query(message.id, text='Вы заблокированы! Попробуйте выключить телефон. 😉', show_alert=True)
    else:
        start(message) # If no have data from user - created

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
    buy = types.InlineKeyboardButton(text="Пополнить баланс", callback_data="buy")
    help = types.InlineKeyboardButton(text="help", callback_data="help")
    close_menu_button = types.InlineKeyboardButton(text="Закрыть меню ✖️", callback_data="close_menu")
    keyboard.add(model, time_limit, reset, stat, buy, help, close_menu_button)
    bot.send_message(message.chat.id, "Настройки ChatGPT:", reply_markup=keyboard)

# Submenu at Main Menu - Model
def model(call):
    keyboard = types.InlineKeyboardMarkup(row_width=1) # 3
    gpt4_1 = types.InlineKeyboardButton(text="ChatGPT 4 Turbo 1106", callback_data="gpt4_1")
    # gpt4 = types.InlineKeyboardButton(text="ChatGPT 4 0613", callback_data="gpt4")
    gpt3_5 = types.InlineKeyboardButton(text="ChatGPT 3.5 Turbo", callback_data="gpt3_5")
    keyboard.add(gpt4_1, gpt3_5) # gpt4
    back_button = types.InlineKeyboardButton(text="<< Назад в главное меню", callback_data="back_menu")
    keyboard.row(back_button)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите модель ChatGPT:", reply_markup=keyboard)

# Back in Submenu Model to Main Menu
def back_menu(call):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    model = types.InlineKeyboardButton(text="Модель ChatGPT", callback_data="model")
    time_limit = types.InlineKeyboardButton(text="Сколько помнить диалог", callback_data="time_limit")
    reset = types.InlineKeyboardButton(text="Сбросить диалог", callback_data="reset")
    stat = types.InlineKeyboardButton(text="Статистика", callback_data="stat")
    buy = types.InlineKeyboardButton(text="Пополнить баланс", callback_data="buy")
    help = types.InlineKeyboardButton(text="help", callback_data="help")
    close_menu_button = types.InlineKeyboardButton(text="Закрыть меню ✖️", callback_data="close_menu")
    keyboard.add(model, time_limit, reset, stat, buy, help, close_menu_button)
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
    back_button = types.InlineKeyboardButton(text="<< Назад в главное меню", callback_data="back_menu")
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
        money = settings[8] # Всего денег на счету
        all_money = settings[9] # Всего внесено денег за все время
        text = f"<b>Версия модели:</b> <i>{model_chat}</i>\n<b>Время хранения диалога</b>: <i>{the_gap} час.</i>\n<b>Использованно токенов за все время:</b> <i>{total_used_token}</i>\n<b>На счету:</b> <i>{money} руб.</i>\n<b>Внесено денег за все время:</b> <i>{all_money} руб.</i>\nСкачать финансовый отчет за 30 дней - /otchet" # <a>http://openai.com</a>  <code>пример</code> <pre> Пример</pre> <i>Пример </i>
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id) # Close Menu
        bot.send_message(call.message.chat.id, text, parse_mode='HTML')

# Script working Menu
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    id = call.from_user.id # telegram id user
    # Model
    if call.data == "model":
        model(call)
    elif call.data == "gpt4":
        model_id="gpt-4"
        add_update_settings(id, model_id=model_id)
        bot.answer_callback_query(call.id, "Вы выбрали ChatGPT 4 0613!")
    elif call.data == "gpt4_1":
        model_id="gpt-4-1106-preview"
        add_update_settings(id, model_id=model_id)
        bot.answer_callback_query(call.id, "Вы выбрали ChatGPT 4 Turbo 1106 preview!")
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
    # Buy
    elif call.data == "buy":
        bot.answer_callback_query(call.id, "В разработке")
        # bot.send_message(call.chat.id, text=f"Извините, но похоже, у вас закончились токены.\n@Shliambur")
        # buy(call)
    # Help
    elif call.data == "help":
        # bot.answer_callback_query(call.id, "В разработке")
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, text=f"Этот бот работает на основе официального ChatGPT   от компании OpenAI\n4 1000ток - 3-6 руб\n3 1000ток 1-2 руб.\nК сожалению, предоставляемый компанией OpenAi API платный, а потому бесплатным ChatGPT быть не может.\n Как экономить:\n1. Использовать короткую память истории или не использовать вообще.\nGPT 3.5 Turbo дешевле раза в 3.\nВ базе хрянится лишь последний слепок вопрос-ответ во выставленном вами временном интервале, для поддержания диалога с чатом. Вы всегда можете это очистить или вообще не использовать. Хранить все переписки экономически дорого, для вашего понимания.")
    # Reset
    elif call.data == "reset":
        reset(call)
    # Statistic
    elif call.data == "stat":
        stat(call)
    # Menu Back
    elif call.data == "back_menu":
        back_menu(call)


#####
start_bot = bot.polling() # Запуск инициализируется в run_bot.py