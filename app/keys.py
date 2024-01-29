import os
from dotenv import load_dotenv
load_dotenv()

token = os.environ.get('TELEGRAM_BOT_CHATGPT_API_KEY') # Telegram key
api_key = os.environ.get('CHATGPT_API_KEY') # OpenAI key-token
azil = os.environ.get('AZIL')
asilisav = os.environ.get('ASILISAV')
admin_user_ids = os.environ.get('ADMIN_USER_IDS')
block = os.environ.get('ALLOWED_TELEGRAM_USER_IDS')
