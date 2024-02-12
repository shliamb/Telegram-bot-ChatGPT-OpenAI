from worker_db import get_settings, add_update_settings
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import LabeledPrice
# from yandex_checkout import Configuration, Payment


##### ПРИ ОПЛАТЕ ТОНАМИ СКИДКА 5% #####



# Настройка API Яндекс.Кассы
# Configuration.account_id = "YOUR_YANDEX_KASSA_ACCOUNT_ID"
# Configuration.secret_key = "YOUR_YANDEX_KASSA_SECRET_KEY"

# Обработчик команды для начала оплаты
@bot.message_handler(commands=['start'])
def start_payment(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Оплатить"))

    bot.send_message(message.chat.id, "Нажмите кнопку 'Оплатить', чтобы произвести оплату", reply_markup=markup)

# Обработчик кнопки оплаты
@bot.message_handler(func=lambda message: message.text == "Оплатить")
def process_payment(message):
    payment = Payment.create({
        "amount": {
            "value": 100.00,
            "currency": "RUB"
        },
        "description": "Оплата за услуги",
        "confirmation": {
            "type": "redirect",
            "return_url": "https://yourwebsite.com/payment/success"
        },
        "capture": True
    })

    bot.send_message(message.chat.id, f"Для оплаты перейдите по ссылке: {payment.confirmation.confirmation_url}")




# Получаем из базы
# settings = get_settings(id)  - получаем с базы статистику
# all_money_spend = settings[9] # Total spending money - вносимые суммы за все время получаем
# money = settings[8]   - наличие на счету, может быть минус, нужно учесть


# оплата  сумма


# Вносим в базу
# new_money = money + сумма
# add_update_settings(all_money_spend=сумма, money_user=new_money) - добавляем в базу при оплате суммы