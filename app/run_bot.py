from keys import token, api_key, white_list, admin_user_ids, block
import time
import sys
import logging
import asyncio
from openai import AsyncOpenAI
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand
from get_time import get_time
from calculation import calculation
from worker_db import (
    adding_user, get_user_by_id, update_user, add_settings, add_discussion, update_settings,
    get_settings, get_discussion, update_discussion, get_exchange, update_exchange, get_last_30_statistics
)
import datetime # позже удалить



client = AsyncOpenAI(api_key=api_key)
TOKEN = token # Telegram
dp = Dispatcher() # All handlers should be attached to the Router (or Dispatcher)
bot = Bot(TOKEN, parse_mode="markdown") # Initialize Bot instance with a default parse mode which will be passed to all API calls



# Get User_ID
def user_id(action) -> int:
    return action.from_user.id

# Show Typing
async def typing(action) -> None:
    await bot.send_chat_action(action.chat.id, action='typing')



# PUSH /START
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await typing(message)

    # Меню
    bot_commands = [
        BotCommand(command="/menu", description="Главное меню"),
        # BotCommand(command="/help", description="Help"),
    ]
    await bot.set_my_commands(bot_commands)


    ###### Get All data user on telegram ######
    id = user_id(message)
    name = message.from_user.username
    full_name = message.from_user.full_name
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    chat_id = message.chat.id
    is_admin = False
    is_block = False
    is_good = 3
    ###### Get All data user on telegram ######

    logging.info(f"User {id} press /start")

    # Checking and added the parameters
    if str(id) in admin_user_ids:
        is_admin = True
        logging.info(f"The user id:{id} is assigned as an admin.")
    if str(id) in block:
        is_block=True
        logging.info(f"The user id:{id} is assigned as an blocked.")

    # Preparing data for the user
    user_data = {"id": id, "name": name, "full_name": full_name, "first_name":first_name,\
                    "last_name": last_name, "chat_id": chat_id, "is_admin": is_admin,\
                    "is_block":is_block, "is_good": is_good}
    
    # If user id has in a Base - update data, else - create user to Base
    is_on_user = await get_user_by_id(id)
    if is_on_user is not None:
        await update_user(id, user_data)
    else:
        await adding_user(user_data)
        await add_settings(id)
        await add_discussion(id)
    
    # Choosing a name user
    about = name if name else (first_name if first_name else (last_name if last_name else "bro"))

    # Checking and added the parameters in Settings to white list users And gives them money
    if str(id) in white_list:
        money = 1000 # Yep!
        updated_data = {"money": money}
        confirmation = await update_settings(id, updated_data) # Gives money
        if confirmation is True: # Подтверждение из worcker_db
            logging.info(f"1000 RUB added, he id is:{id}.")
        else:
            logging.error(f"A 1000 RUB has not added, he id is:{id}.")

    await message.answer(f"Привет {about}! Я *ChatGPT*. Мне можно сразу задать вопрос или настроить - /setup.")



# test user
@dp.message(Command("user"))
async def user(message: types.Message):
    await typing(message)
    id = user_id(message)
    user = await get_user_by_id(id)

    if user:
        id = user.id
        name = user.name
        full_name = user.full_name
        first_name = user.first_name
        last_name = user.last_name
        chat_id = user.chat_id
        is_admin = user.is_admin
        is_block = user.is_block
        is_good = user.is_good
        print(id, name, full_name, first_name, last_name, chat_id, is_admin, is_block, is_good)
    else:
        print("User not found")


# test set
@dp.message(Command("set"))
async def set(message: types.Message):
    await typing(message)
    id = user_id(message)
    user = await get_settings(id)

    if user:
        id = user.id
        temp_chat = user.temp_chat
        frequency = user.frequency
        presence = user.presence
        all_count = user.all_count
        all_token = user.all_token
        the_gap = user.the_gap
        set_model = user.set_model
        give_me_money = user.give_me_money
        money = user.money
        all_in_money = user.all_in_money
        flag_stik = user.flag_stik
        print(id, temp_chat, frequency, presence, flag_stik, all_count, all_token, the_gap,\
               set_model, give_me_money, money, all_in_money)
    else:
        print("Settings not found")


# test desc
@dp.message(Command("desc"))
async def set(message: types.Message):
    await typing(message)
    id = user_id(message)
    data = await get_discussion(id)

    if data:
        id = data.id
        discus = data.discus
        timestamp = data.timestamp
        print(id, discus, timestamp)
    else:
        print("Descussion not found")

# Test 30 day statistics for user id
@dp.message(Command("30"))
async def set(message: types.Message):
    await typing(message)
    id = user_id(message)
    data = await get_last_30_statistics(id)
    if data:
        for statistic in data:
            print(statistic.id, statistic.time, statistic.use_model, statistic.sesion_token,\
                   statistic.price_1_tok, statistic.price_sesion_tok, statistic.users_telegram_id )
    else:
        print("Нет данных для этого пользователя")



# test ex
@dp.message(Command("ex"))
async def ex(message: types.Message):
    await typing(message)
    id = user_id(message)
    data = await get_exchange()

    if data:
        id = data.id
        timestamp = data.timestamp
        rate = data.rate
        print(id, timestamp, rate)
    else:
        print("ex rate not found")


# test ex update
@dp.message(Command("upex"))
async def upex(message: types.Message):
    await typing(message)
    data = datetime.datetime.strptime('2024-02-05 04:44:23.791821', '%Y-%m-%d %H:%M:%S.%f')
    timer = {"timestamp": data}
    await update_exchange(1, timer)


# # Admin statistic lite menu /admin
# @dp.message(Command("admin"))
# async def admin(message: types.Message):
#     await typing(message)
#     id = user_id(message)
#     data = read_tele_user(id)
#     if data is not None:
#         if data[5] == True:
#             await message.answer("Статистика: [/admin_static]\n Скачать: [/log] Очистить логи: [/clearlog]") 
#         else:
#             await message.answer("Извините, вас нет в списках администраторов.")










#### WORK MENU ####

from keyboards import (
    main_menu, sub_setings, sub_balance, back_to_main, back_to_setings,\
    sub_setings_model, sub_setings_time, sub_setings_creativ, sub_setings_repet, sub_setings_repet_all, sub_add_money
)


# Main menu strat
@dp.message(Command('setup', 'menu', 'setings'))
async def start(message: types.Message):
    await main_menu(bot, message)

# Back to main
@dp.callback_query(lambda c: c.data == 'back_to_main')
async def process_back_to_main(callback_query: types.CallbackQuery):
    await back_to_main(bot, callback_query)
    await bot.answer_callback_query(callback_query.id)

# Close menu
@dp.callback_query(lambda c: c.data == 'close')
async def close_main(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    await bot.delete_message(chat_id=chat_id, message_id=message_id) # Удалить и меню и сообщение
    await bot.answer_callback_query(callback_query.id)
####

#### SETTINGS #### 
# Settings
@dp.callback_query(lambda c: c.data == 'sub_setings')
async def process_sub_setings(callback_query: types.CallbackQuery):
    #await callback_query.answer("Нажали кнопку ") # Выводит уведомление быстрое
    await sub_setings(bot, callback_query)
    await bot.answer_callback_query(callback_query.id)

# Back to Settings
@dp.callback_query(lambda c: c.data == 'back_to_setings')
async def process_back_to_settings(callback_query: types.CallbackQuery):
    await back_to_setings(bot, callback_query)
    await bot.answer_callback_query(callback_query.id)
####

# Settings - model
@dp.callback_query(lambda c: c.data == 'model')
async def process_sub_settings_modell(callback_query: types.CallbackQuery):
    await sub_setings_model(bot, callback_query)
    await bot.answer_callback_query(callback_query.id)

# Settings - model - gpt-4-1106-preview
@dp.callback_query(lambda c: c.data == 'gpt-4-1106-preview')
async def process_sub_settings_modell_1106(callback_query: types.CallbackQuery):
    # chat_id = callback_query.message.chat.id
    # message_id = callback_query.message.message_id
    # await bot.send_chat_action(chat_id, action='typing')
    id = user_id(callback_query)
    # await bot.send_chat_action(chat_id, action='typing')
    updated_data = {"set_model": "gpt-4-1106-preview"}
    await update_settings(id, updated_data)
    await callback_query.answer("Установлена модель - gpt-4-1106-preview")
    await bot.answer_callback_query(callback_query.id)

# Settings - model - gpt-4-0125-preview
@dp.callback_query(lambda c: c.data == 'gpt-4-0125-preview')
async def process_sub_settings_modell_0125(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"set_model": "gpt-4-0125-preview"}
    await update_settings(id, updated_data)
    await callback_query.answer("Установлена модель - gpt-4-0125-preview")
    await bot.answer_callback_query(callback_query.id)

# Settings - model - gpt-3.5-turbo-0613
@dp.callback_query(lambda c: c.data == 'gpt-3.5-turbo-0613')
async def process_sub_settings_modell_0125(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"set_model": "gpt-3.5-turbo-0613"}
    await update_settings(id, updated_data)
    await callback_query.answer("Установлена модель - gpt-3.5-turbo-0613")
    await bot.answer_callback_query(callback_query.id)
####

# Settings - time
@dp.callback_query(lambda c: c.data == 'time')
async def process_sub_settings_time(callback_query: types.CallbackQuery):
    await sub_setings_time(bot, callback_query)
    await bot.answer_callback_query(callback_query.id)

# Settings - time - no
@dp.callback_query(lambda c: c.data == 'no_time')
async def process_sub_settings_time_no(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"the_gap": 0}
    await update_settings(id, updated_data)
    await callback_query.answer("Каждый вопрос для ChatGPT будет новым.")
    await bot.answer_callback_query(callback_query.id)

# Settings - time - 5 min
@dp.callback_query(lambda c: c.data == '5_time')
async def process_sub_settings_time_5(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"the_gap": 0.05}
    await update_settings(id, updated_data)
    await callback_query.answer("Диалог будет актуальным в течении 5 минут.")
    await bot.answer_callback_query(callback_query.id)

# Settings - time - 15 min
@dp.callback_query(lambda c: c.data == '15_time')
async def process_sub_settings_time_15(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"the_gap": 0.15}
    await update_settings(id, updated_data)
    await callback_query.answer("Диалог будет актуальным в течении 15 минут.")
    await bot.answer_callback_query(callback_query.id)

# Settings - time - 30 min
@dp.callback_query(lambda c: c.data == '30_time')
async def process_sub_settings_time_30(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"the_gap": 0.30}
    await update_settings(id, updated_data)
    await callback_query.answer("Диалог будет актуальным в течении 30 минут.")
    await bot.answer_callback_query(callback_query.id)
####

# Settings - Creativ
@dp.callback_query(lambda c: c.data == 'creativ')
async def process_sub_settings_creativ(callback_query: types.CallbackQuery):
    await sub_setings_creativ(bot, callback_query)
    await bot.answer_callback_query(callback_query.id)

# Settings - Creativ - no
@dp.callback_query(lambda c: c.data == 'creativ_0')
async def process_sub_settings_creativ_0(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"temp_chat": 0}
    await update_settings(id, updated_data)
    await callback_query.answer("100% консервативности в ответах.")
    await bot.answer_callback_query(callback_query.id)

# Settings - Creativ - creativ_3
@dp.callback_query(lambda c: c.data == 'creativ_3')
async def process_sub_settings_creativ_3(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"temp_chat": 0.3}
    await update_settings(id, updated_data)
    await callback_query.answer("Консервативность 70%, Разнообразие 30%")
    await bot.answer_callback_query(callback_query.id)

# Settings - Creativ - creativ_5
@dp.callback_query(lambda c: c.data == 'creativ_5')
async def process_sub_settings_creativ_5(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"temp_chat": 0.5}
    await update_settings(id, updated_data)
    await callback_query.answer("Консервативность 50%, Разнообразие 50%")
    await bot.answer_callback_query(callback_query.id)

# Settings - Creativ - creativ_7
@dp.callback_query(lambda c: c.data == 'creativ_7')
async def process_sub_settings_creativ_7(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"temp_chat": 0.7}
    await update_settings(id, updated_data)
    await callback_query.answer("Консервативность 30%, Разнообразие 70%")
    await bot.answer_callback_query(callback_query.id)

# Settings - Creativ - creativ_1
@dp.callback_query(lambda c: c.data == 'creativ_1')
async def process_sub_settings_creativ_1(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"temp_chat": 1}
    await update_settings(id, updated_data)
    await callback_query.answer("100% Разнообразия в ответах.")
    await bot.answer_callback_query(callback_query.id)
####
    

# Settings - repet
@dp.callback_query(lambda c: c.data == 'repet')
async def process_sub_settings_repet(callback_query: types.CallbackQuery):
    await sub_setings_repet(bot, callback_query)
    await bot.answer_callback_query(callback_query.id)

# Settings - repet - no
@dp.callback_query(lambda c: c.data == 'repet_0')
async def process_sub_settings_repet_0(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"frequency": 0}
    await update_settings(id, updated_data)
    await callback_query.answer("Минимальное повторение в ответе.")
    await bot.answer_callback_query(callback_query.id)

# Settings - repet - 3
@dp.callback_query(lambda c: c.data == 'repet_3')
async def process_sub_settings_repet_3(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"frequency": 0.3}
    await update_settings(id, updated_data)
    await callback_query.answer("На 30% возможных повторений больше в ответе.")
    await bot.answer_callback_query(callback_query.id)

# Settings - repet - 5
@dp.callback_query(lambda c: c.data == 'repet_5')
async def process_sub_settings_repet_5(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"frequency": 0.5}
    await update_settings(id, updated_data)
    await callback_query.answer("На 50% возможных повторений больше в ответе.")
    await bot.answer_callback_query(callback_query.id)

# Settings - repet - 7
@dp.callback_query(lambda c: c.data == 'repet_7')
async def process_sub_settings_repet_7(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"frequency": 0.7}
    await update_settings(id, updated_data)
    await callback_query.answer("На 70% возможных повторений больше в ответе.")
    await bot.answer_callback_query(callback_query.id)

# Settings - repet - 1
@dp.callback_query(lambda c: c.data == 'repet_1')
async def process_sub_settings_repet_1(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"frequency": 1}
    await update_settings(id, updated_data)
    await callback_query.answer("На 100% возможных повторений больше в ответе.")
    await bot.answer_callback_query(callback_query.id)
####


# Settings - presence
@dp.callback_query(lambda c: c.data == 'repet_all')
async def process_sub_settings_repet_all(callback_query: types.CallbackQuery):
    await sub_setings_repet_all(bot, callback_query)
    await bot.answer_callback_query(callback_query.id)

# Settings - presence - no
@dp.callback_query(lambda c: c.data == 'repet_all_0')
async def process_sub_settings_repet_all_0(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"presence": 0}
    await update_settings(id, updated_data)
    await callback_query.answer("Минимальное повторение в ответах.")
    await bot.answer_callback_query(callback_query.id)

# Settings - presence - 3
@dp.callback_query(lambda c: c.data == 'repet_all_3')
async def process_sub_settings_repet_all_3(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"presence": 0.3}
    await update_settings(id, updated_data)
    await callback_query.answer("На 30% возможных повторений больше в ответах.")
    await bot.answer_callback_query(callback_query.id)

# Settings - presence - 5
@dp.callback_query(lambda c: c.data == 'repet_all_5')
async def process_sub_settings_repet_all_5(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"presence": 0.5}
    await update_settings(id, updated_data)
    await callback_query.answer("На 50% возможных повторений больше в ответах.")
    await bot.answer_callback_query(callback_query.id)

# Settings - presence - 7
@dp.callback_query(lambda c: c.data == 'repet_all_7')
async def process_sub_settings_repet_all_7(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"presence": 0.7}
    await update_settings(id, updated_data)
    await callback_query.answer("На 70% возможных повторений больше в ответах.")
    await bot.answer_callback_query(callback_query.id)

# Settings - presence - 1
@dp.callback_query(lambda c: c.data == 'repet_all_1')
async def process_sub_settings_repet_all_1(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"presence": 1}
    await update_settings(id, updated_data)
    await callback_query.answer("На 100% возможных повторений больше в ответах.")
    await bot.answer_callback_query(callback_query.id)
####


# Settings - flag_stik
@dp.callback_query(lambda c: c.data == 'flag_stik')
async def process_sub_settings_flag_stik(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    data = await get_settings(id)
    if data:
        flag_stik = data.flag_stik
    if flag_stik == True:
        updated_data = {"flag_stik": False}
        await update_settings(id, updated_data)
        await callback_query.answer("Строка статистики в ответе отключена.")
    if flag_stik == False:
        updated_data = {"flag_stik": True}
        await update_settings(id, updated_data)
        await callback_query.answer("Строка статистики в ответе включена.")
        await bot.answer_callback_query(callback_query.id)
####


# Settings - reset dialog
@dp.callback_query(lambda c: c.data == 'sub_dialog')
async def process_sub_dialog(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    updated_data = {"discus": None}
    await update_discussion(id, updated_data)
    await callback_query.answer("Ваш диалог с ChatGPT сброшен.")
    await bot.answer_callback_query(callback_query.id)
####

# Settings - finansi
@dp.callback_query(lambda c: c.data == 'sub_balance')
async def process_sub_balance(callback_query: types.CallbackQuery):
    await sub_balance(bot, callback_query)
    await bot.answer_callback_query(callback_query.id)
####

# Settings - my_many
@dp.callback_query(lambda c: c.data == 'my_many')
async def process_sub_settings_my_many(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    data = await get_settings(id)
    if data:
        money = round(data.money, 2)
        await bot.send_message(callback_query.from_user.id, f"<b>На вашем счету:\n{money}</b> RUB\n", parse_mode="HTML")
    await bot.answer_callback_query(callback_query.id)
####

# Settings - add_money
@dp.callback_query(lambda c: c.data == 'add_money')
async def process_sub_settings_add_money(callback_query: types.CallbackQuery):
    await sub_add_money(bot, callback_query)
    await bot.answer_callback_query(callback_query.id)

# Settings - add_money - 100
@dp.callback_query(lambda c: c.data == 'many_100')
async def process_sub_settings_add_money_100(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    await callback_query.answer("100")
    await bot.answer_callback_query(callback_query.id)

# Settings - add_money - 200
@dp.callback_query(lambda c: c.data == 'many_200')
async def process_sub_settings_add_money_200(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    await callback_query.answer("200")
    await bot.answer_callback_query(callback_query.id)

# Settings - add_money - 500
@dp.callback_query(lambda c: c.data == 'many_500')
async def process_sub_settings_add_money_500(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    await callback_query.answer("500")
    await bot.answer_callback_query(callback_query.id)

# Settings - add_money - 700
@dp.callback_query(lambda c: c.data == 'many_700')
async def process_sub_settings_add_money_700(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    await callback_query.answer("700")
    await bot.answer_callback_query(callback_query.id)

# Settings - add_money - 1000
@dp.callback_query(lambda c: c.data == 'many_1000')
async def process_sub_settings_add_money_1000(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    await callback_query.answer("1000")
    await bot.answer_callback_query(callback_query.id)

# Settings - add_money - 2000
@dp.callback_query(lambda c: c.data == 'many_2000')
async def process_sub_settings_add_money_2000(callback_query: types.CallbackQuery):
    id = user_id(callback_query)
    await callback_query.answer("2000")
    await bot.answer_callback_query(callback_query.id)



####

# Settings - about
@dp.callback_query(lambda c: c.data == 'sub_about')
async def process_sub_about(callback_query: types.CallbackQuery):
    #await sub_about(bot, callback_query)
    await bot.send_message(callback_query.from_user.id, f"<b>🤙🏼 О боте</b>\nБот работает на API OpenAI.", parse_mode="HTML")
    await bot.answer_callback_query(callback_query.id)










# Message to OpenAI
@dp.message()
async def handle_message(message: types.Message):
    await typing(message)
    id = user_id(message)
    logging.info(f"User {id} - {message.text}")

    if message.text is not None and not message.text.startswith('/') and isinstance(message.text, str):

        data = await get_settings(id)
        if data is not None:
            temp_chat = data.temp_chat
            frequency = data.frequency
            presence = data.presence
            all_count = data.all_count
            all_token = data.all_token
            the_gap = data.the_gap
            #set_model = data.set_model
            set_model = "gpt-4-1106-preview"
            give_me_money = data.give_me_money
            money = data.money
            all_in_money = data.all_in_money
            flag_stik = data.flag_stik

            if money > 0 and money != 0:
                cache = []
                ged = await get_discussion(id)

                if ged is not None:
                    # Time in a DB
                    discus = ged.discus # Text data
                    date_db = ged.timestamp  # Время из базы записи
                    day_db = date_db.strftime("%Y-%m-%d")
                    time_db = date_db.strftime("%H.%M")
                    # Time now
                    now = get_time()
                    if now:
                        date_now = now['day']
                        time_now = now['time']

                    difference = float(time_now) - float(time_db) # Difference
                    if day_db == date_now and difference < the_gap and discus is not None:
                        cache.append(discus)

                # Question to OpenAI
                cache.append(f"{message.text}\n")
                format_session_data = ' '.join(cache)

                # OpenAI
                await typing(message)
                answer = await client.chat.completions.create(
                    messages = [{"role": "user", "content": format_session_data,}],
                    model = set_model,
                    temperature = temp_chat,      # консервативность - разнообразие
                    frequency_penalty = frequency,  # 0 - допускает повторение слов и фраз в рамках данного ответа, 
                    presence_penalty = presence, # 0 - допускает повторение слов и фраз из прошлых ответов
                    #max_tokens=1000,
                    )
                
                await typing(message)
                if answer is not None:
                    ######### This date from Open AI ########
                    text = answer.choices[0].message.content # Text response AI
                    model_version = answer.model # Model in answer
                    used_tokens = answer.usage.total_tokens 
                    # completion_tokens = chat_completion.usage.completion_tokens
                    # prompt_tokens = chat_completion.usage.prompt_tokens
                    ######### This date from Open AI ########

                    stik = f"\n_{model_version}_\n_{used_tokens} ток._\n[/setup]" if flag_stik else ""
                    send = f"{text}\n\n{stik}"
                    await message.answer(send)

                data = {
                    "id": id,
                    "model_version": model_version,
                    "used_tokens": used_tokens,
                    "all_count": all_count,
                    "all_token": all_token,
                    "give_me_money": give_me_money,
                    "money": money,
                    "all_in_money": all_in_money,
                }
                rashod = await calculation(data)
                print("Rashod:",rashod)



                # Push update talking to DB
                cache.append(f"{text}\n")
                clear_data = ' '.join(cache)
                updated_data = {
                    "discus": clear_data,
                    # "timestamp": timestamp,
                    }
                await update_discussion(id, updated_data)
                cache = []

            if money < 0 and money == 0:
                await message.answer("Извините, но похоже, у вас нулевой баланс.\n Пополнить - [/setup]")
                logging.info(f"User {id} her money is finish.")
        if data is None:
            await command_start_handler(message)
            logging.info(f"User {id} is not on DB, added.")
    else:
        await message.answer("Извините, сообщение в неподдерживаемом формате.")
        logging.error(f"Error, not correct message from User whose id is {id}")





# Main polling
async def main() -> None:
    await dp.start_polling(bot)

# Start and Restart
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout) # При деплое закомментировать
    #logging.basicConfig(level=logging.INFO, filename='log/app.log', filemode='a', format='%(levelname)s - %(asctime)s - %(name)s - %(message)s',) # При деплое активировать логирование в файл
    retries = 5
    while retries > 0:
        try:
            asyncio.run(main())
            break # Если выполнение успешно - выходим из цикла.
        except Exception as e:
            logging.error(f"An error occurred: {e}. Restarting after a delay...")
            retries -= 1
            
            if retries > 0:
                time.sleep(5)  # Ожидаем перед попыткой перезапуска
