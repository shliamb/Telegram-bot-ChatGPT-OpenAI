import os
import telebot

# Telegram key
token = os.environ.get('TELEGRAM_BOT_CHATGPT_API_KEY')
bot = telebot.TeleBot(token)

# OpenAI key-token
api_key = os.environ.get('CHATGPT_API_KEY')