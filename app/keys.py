import os
from dotenv import load_dotenv
load_dotenv()

token = os.environ.get('TELEGRAM_BOT_CHATGPT_API_KEY') # Telegram key
api_key = os.environ.get('CHATGPT_API_KEY') # OpenAI key-token - установить только на сервере руками
white_list = os.environ.get('WHITE_LIST')
admin_user_ids = os.environ.get('ADMIN_USER_IDS')
block = os.environ.get('ALLOWED_TELEGRAM_USER_IDS')
oppas = os.environ.get('OPPAS')
user_db = os.environ.get('USER_DB')
paswor_db = os.environ.get('PASWOR_DB')


# В корне есть файл .env.example, при деплое меняем имя на .env тут же станет скрытым. В папке Cntrl + H (Linux),
# но VisualStudio увидит его. Внутри проставляем свои ключи, но ключ на OpenAI устанавливаем только на сервере вручную. 
# Т.е. заходим на сервер и ручками ставим ключ. Если ключ от OpenAI окажется в  GitHab - тут же в панеле управления OpenAI
# удалится. Так хоть как то защищаем ключи в виртуальном окружении.