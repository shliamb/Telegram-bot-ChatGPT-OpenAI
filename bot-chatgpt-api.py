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


# Options chatGPT
patch = "Ответ не больше одного предложения." # Пока проверяю, экономлю)
temp = 0.7
# temperature = 0, консервативные, наиболее вероятное следующее слово, ответы более детерминированные и менее разнообразные.
# temperature = 1, увеличивает случайность в выборе слов, более разнообразные и творческие ответы, неожиданные результаты, вероятность нерелевантного или некорректного контента.
model = "gpt-3.5-turbo"
# gpt-4-1106-preview   150,000 TPM    500 RPM  (turbo)
# gpt-3.5-turbo        60,000 TPM     500 RPM  (cheap)
# gpt-4 


# Подготовка логирования
logging.basicConfig(filename='bot.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# Вызов и вид меню /setup
@bot.message_handler(commands=['setup'])
def send_welcome(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1) # Колличество кнопок в одной строке
    version_chat = types.InlineKeyboardButton(text="Выбрать версию ChatGPT", callback_data="version_chat")
    version_dialog = types.InlineKeyboardButton(text="Режим: Один вопрос /  Диалог", callback_data="mode_dialog")
    version_creativity = types.InlineKeyboardButton(text="Установить уровень творчества", callback_data="level_creativity")
    keyboard.add(version_chat, version_dialog, version_creativity)
    bot.send_message(message.chat.id, "Настройки ChatGPT:\nВыберите опцию для настройки.", reply_markup=keyboard)


# Работа Меню
@bot.callback_query_handler(func=lambda call: True) # Декоратор Telebot ожидает и обрабытывает запросы от callback_data
def callback_inline(call):
    if call.data == "version_chat":
        bot.answer_callback_query(call.id, "Вы нажали кнопку version_chat!")
    logger.info(f" - call_dat:'{call.data}' - user_name:{call.from_user.username} - user_id:{call.from_user.id}")


# Принимает message - chatgpt - возвращает результат
@bot.message_handler(func=lambda message: message.text is not None and not message.text.startswith('/')) # Декоратор Telebot принимает все, кроме того, что начинается на /
def handle_message(message):
    #bot.send_message(message.chat.id, "hi")
    logger.info(f" - message_text:'{message.text}' - user_name:{message.from_user.username} - user_id:{message.from_user.id}")
    #bot.reply_to(message, "hi")
    # Собираем запрос Json к API Openai
    question = message.text + " " +patch
    #print(question)
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
    #print("\n", first_choice_message, "\n")
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