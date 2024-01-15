import os
import time
import telebot
from telebot import types
import requests
import json
import logging


# Токены и key в переменных окружения
token = os.environ.get('TELEGRAM_BOT_CHATGPT_API_KEY')
bot = telebot.TeleBot(token)
api_key = os.environ.get('CHATGPT_API_KEY')
url = 'https://api.openai.com/v1/chat/completions'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}


# Options ChatGPT
patch = "Ответ не больше трех предложений." # Пока проверяю, экономлю)
temp = 0.7
# temperature = 0, консервативные, наиболее вероятное следующее слово, ответы более детерминированные и менее разнообразные.
# temperature = 1, увеличивает случайность в выборе слов, более разнообразные и творческие ответы, неожиданные результаты, вероятность нерелевантного или некорректного контента.
model = "gpt-3.5-turbo"
# gpt-4-1106-preview   150,000 TPM    500 RPM  (turbo)
# gpt-3.5-turbo        60,000 TPM     500 RPM  (cheap)
# gpt-4 


# Подготовка логирования
logging.basicConfig(filename='log/bot.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)



flag_menu = False # Флаг, по которому будет ясно, запущена ли клавиатура, пока что так, ничего лучше не придумал

# Вызов меню /setup
@bot.message_handler(commands=['setup'])

# Главное меню
def main_menu(message):
    global flag_menu
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    version_chat = types.InlineKeyboardButton(text="Версия ChatGPT 🦾", callback_data="version_chat")
    version_dialog = types.InlineKeyboardButton(text="Режим ответа 🗣", callback_data="mode_dialog")
    version_creativity = types.InlineKeyboardButton(text="Уровень творчества 👻", callback_data="level_creativity")
    close_menu_button = types.InlineKeyboardButton(text="Закрыть меню ✖️", callback_data="close_menu")
    keyboard.add(version_chat, version_dialog, version_creativity, close_menu_button)
    if flag_menu == False:
        bot.send_message(message.chat.id, "Выберите опцию для настройки ChatGPT:", reply_markup=keyboard)
        flag_menu = True
    else:
        #breakpoint
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Выберите версию ChatGPT:", reply_markup=keyboard)


# Под меню version_chat
def version_submenu(call):
    global flag_menu
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    gpt_4_1106_preview = types.InlineKeyboardButton(text="GPT-4 1106", callback_data="gpt_4_1106_preview")
    gpt_3_5_turbo  = types.InlineKeyboardButton(text="GPT-3.5 turbo", callback_data="gpt_3_5_turbo")
    gpt_4 = types.InlineKeyboardButton(text="GPT-4", callback_data="gpt_4")
    keyboard.add(gpt_3_5_turbo, gpt_4_1106_preview, gpt_4) # По условиям row_width
    back_button = types.InlineKeyboardButton(text="Назад в главное меню", callback_data="back_menu") # Сначало определяем кнопку back_button
    keyboard.row(back_button) # Затем добавляем в конец, без условий row_width, в отдельную строку
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите версию ChatGPT:", reply_markup=keyboard)
    flag_menu = True

# Закрыть клавиатуру
@bot.callback_query_handler(func=lambda call: call.data == "close_menu")
def handle_close_menu(call):
    global flag_menu
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    flag_menu = False


# Работа Меню
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global flag_menu
    chat_id = call.message.chat.id if call.message is not None else None
    message_id = call.message.message_id if call.message is not None else None
    inline_message_id = call.inline_message_id if call.inline_message_id is not None else None

    if call.data == "version_chat":
        version_submenu(call)
    elif call.data == "mode_dialog":
        bot.answer_callback_query(call.id, "Вы нажали кнопку mode_dialog!")
    elif call.data == "back_menu":
        if chat_id:
            main_menu(call.message)
            flag_menu = False
        elif inline_message_id:
            print("Обработка для inline-режима") # Обработка для inline-режима
            
    logger.info(f" - call_dat:'{call.data}' - user_name:{call.from_user.username} - user_id:{call.from_user.id}")


# Принимает message - chatgpt - возвращает результат
@bot.message_handler(func=lambda message: message.text is not None and not message.text.startswith('/')) # Декоратор Telebot принимает все, кроме того, что начинается на /
def handle_message(message):
    # bot.send_message(message.chat.id, "hi")
    logger.info(f" - message_text:'{message.text}' - user_name:{message.from_user.username} - user_id:{message.from_user.id}")
    # bot.reply_to(message, "hi")
    # Собираем запрос Json к API Openai
    question = message.text + " " +patch
    # print(question)
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": question}],
        "temperature": temp,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))

    response_data = response.json()  # Разбираем JSON-ответ

    first_choice_message = response_data['choices'][0]['message']['content']
    # print("\n", first_choice_message, "\n")
    bot.reply_to(message, first_choice_message)


# Запуск прослушивания api, если соединение отваливается перезапуск, проверенно - работает
while True:
    try:
        bot.polling(none_stop=True, timeout=10)  # Меньшее значение таймаута
        break  # Если polling успешно завершился, выходим из цикла
    except requests.exceptions.ReadTimeout:
        logger.error("Превышено время ожидания запроса. Перезапускаем соединение...")
        print("Превышено время ожидания запроса. Перезапускаем соединение...")
        time.sleep(5)  # Подождать немного перед перезапуском
    except Exception as e:
        logger.exception("Произошла непредвиденная ошибка:")
        print(f"Произошла ошибка: {e}")
        break  # Выход из цикла в случае других ошибок


    # user_id = message.from_user.id
    # user_first_name = message.from_user.first_name  # Имя пользователя
    # user_last_name = message.from_user.last_name  # Фамилия пользователя (может быть None)
    # user_username = message.from_user.username  # Юзернейм пользователя (может быть None)
    # chat_id = message.chat.id