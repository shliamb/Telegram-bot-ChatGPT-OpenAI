import os
from dotenv import load_dotenv
load_dotenv()

token = os.environ.get('TELEGRAM_BOT_CHATGPT_API_KEY') # Telegram key
api_key = os.environ.get('CHATGPT_API_KEY') # OpenAI key-token - установить только на сервере руками
white_list = os.environ.get('WHITE_LIST')
admin_user_ids = os.environ.get('ADMIN_USER_IDS')
block = os.environ.get('ALLOWED_TELEGRAM_USER_IDS')
pass_psgresql = os.environ.get('PASS_POSTGRESQL')
payments_token = os.environ.get('PAYMENTS_TOKEN')
receiver_yoomoney = os.environ.get('YOOMONEY')
token_yoomoney = os.environ.get('TOKEN_YOOMONEY')
wallet_pay_token = os.environ.get('WALLET_PAY')


# В корне есть файл .env.example, при деплое меняем имя на .env тут же станет скрытым. В папке Cntrl + H (Linux),
# но VisualStudio увидит его. Внутри проставляем свои ключи, но ключ на OpenAI устанавливаем только на сервере вручную. 
# Т.е. заходим на сервер и ручками ставим ключ. Если ключ от OpenAI окажется в  GitHab - тут же в панеле управления OpenAI
# удалится. Так хоть как то защищаем ключи в виртуальном окружении.