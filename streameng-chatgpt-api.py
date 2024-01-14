# Strem
#import requests
#import json
import os
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key = os.environ.get('CHATGPT_API_KEY') # Переменная окружения,
)
question = "Как тебя зовут, меня Саша"
model = "gpt-3.5-turbo" # or gpt-3.5-turbo
# gpt-4-1106-preview   150,000 TPM    500 RPM  (turbo)
# gpt-3.5-turbo        60,000 TPM     500 RPM  (cheap)
# gpt-4                10,000 TPM     500 RPM  (expensive)

async def main():
    stream = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": question}],
        stream=True,
    )
    async for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")


asyncio.run(main())


#####################

import os
import asyncio
from openai import AsyncOpenAI
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

telegram_bot_chatgpt_api_key = os.environ.get('TELEGRAM_BOT_CHATGPT_API_KEY')

# Инициализация клиента OpenAI
client = AsyncOpenAI(api_key=os.environ.get('CHATGPT_API_KEY'))
model = "gpt-3.5-turbo"  # Модель OpenAI

# Хранение истории диалогов
dialogues = {}

# Функция для команды /start
async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    dialogues[user_id] = []  # Инициализация новой истории диалога
    await update.message.reply_text('Привет! Как я могу помочь?')

# Функция для команды /reset
async def reset(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    dialogues[user_id] = []  # Сброс истории диалога
    await update.message.reply_text('Диалог сброшен.')

# Функция для обработки сообщений
async def message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_message = update.message.text
    dialogues[user_id].append({"role": "user", "content": user_message})

    # Создание потока для получения ответа
    stream = await client.chat.completions.create(
        model=model,
        messages=dialogues[user_id],
        stream=True,
    )

    # Получение и обработка ответа
    bot_response = ""
    async for chunk in stream:
        if chunk.choices[0].delta.content:
            bot_response += chunk.choices[0].delta.content

    dialogues[user_id].append({"role": "assistant", "content": bot_response})
    await update.message.reply_text(bot_response)

# Главная функция
def main():
    updater = Updater(telegram_bot_chatgpt_api_key)  # Ключ бота

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("reset", reset))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    asyncio.run(main())
