from worker_db import get_settings, update_settings
import logging
import asyncio


# Обработка данных при оплате картой РФ
async def add_money_by_card(data):

    # Получаем переданые данные из функции
    # user_uuid = data.get('user_uuid')
    id = data.get('id')
    percent = data.get('percent')
    summ = data.get('summ')
    remains_pay = float(summ) * float(percent) / 100 # Расчет процента
    new_summ = float(summ) - remains_pay # Сумма пойдет в общий счет 

    # Получаем из DB настройки пользователя
    user = await get_settings(id)
    if user:
        #give_me_money = user.give_me_money
        all_money = user.money + new_summ # Теперь всего на счету
        all_in_money = user.all_in_money + new_summ # Всего внесенно за все время

    # Формируем данные для перезаписи в базу
    updated_data = {
        "money": all_money,
        "all_in_money": all_in_money,
    }

    # Переписываем данные
    await update_settings(id, updated_data)
    logging.info("Money added for user settings")

    return new_summ



# Обработка данных при оплате WALLET PAY
async def add_money_wallet_pay(data):

    # Получаем переданые данные из функции
    # order = data.get('order')
    # currency = data.get('currency')
    # wallet_uuid = data.get('wallet_uuid')
    summ = data.get('summ')
    id = data.get('id')

    new_summ = float(summ) # Сумма пойдет в общий счет 

    # Получаем из DB настройки пользователя
    user = await get_settings(id)
    if user:
        #give_me_money = user.give_me_money
        all_money = user.money + new_summ # Теперь всего на счету
        all_in_money = user.all_in_money + new_summ # Всего внесенно за все время

    # Формируем данные для перезаписи в базу
    updated_data = {
        "money": all_money,
        "all_in_money": all_in_money,
    }

    # Переписываем данные
    await update_settings(id, updated_data)
    logging.info("Money added for user settings")

    return new_summ