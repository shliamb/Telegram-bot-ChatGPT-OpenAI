from keys import token, api_key, white_list, admin_user_ids, block
import time
import sys
import logging
import asyncio
from openai import AsyncOpenAI
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from worker_db import adding_user, get_user_by_id, update_user, add_settings, add_discussion, update_settings,\
get_settings, get_discussion, update_discussion
from get_time import get_time
from models import UsersTelegram


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
        confirmation = await update_user(id, user_data)
        if confirmation is True:
            logging.info(f"The user id is:{id} data has been updated.")
        else:
            logging.error(f"The user id is:{id} her data is not update.")
    else:
        confirmation = await adding_user(user_data)
        if confirmation is True:
            logging.info(f"A new user has been added, he id is:{id}.")
        else:
            logging.error(f"A new user has not added, he id is:{id}.")

        confirmation = await add_settings(id)
        if confirmation is True:
            logging.info(f"A id user to settings added, he id is:{id}.")
        else:
            logging.error(f"A id user has not added to settings, he id is:{id}.")

        confirmation = await add_discussion(id)
        if confirmation is True:
            logging.info(f"A id user to discussion added, he id is:{id}.")
        else:
            logging.error(f"A id user has not added to discussion, he id is:{id}.")
    


    # Choosing a name user
    about = name if name else (first_name if first_name else (last_name if last_name else "bro"))

    # Checking and added the parameters in Settings to white list users And gives them money
    if str(id) in white_list:
        money = 1000 # Yep!
        updated_data = {"money": money}
        confirmation = await update_settings(id, updated_data) # Gives money
        if confirmation is True:
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
        print(id, temp_chat, frequency, presence, all_count, all_token, the_gap, set_model, give_me_money, money, all_in_money)
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


# Message to OpenAI
@dp.message()
async def handle_message(message: types.Message):
    await typing(message)
    id = user_id(message)
    logging.info(f"User {id} - {message.text}")
    data = await get_settings(id)
    if data:
        temp_chat = data.temp_chat
        frequency = data.frequency
        presence = data.presence
        all_count = data.all_count
        all_token = data.all_token
        the_gap = data.the_gap
        set_model = data.set_model
        give_me_money = data.give_me_money
        money = data.money
        all_in_money = data.all_in_money

        flag_stik = False

    if message.text is not None and not message.text.startswith('/') and isinstance(message.text, str):
        if money is not None:
            if money > 0 and money != 0:
                cache = []




                ged = await get_discussion(id)
                if ged:
                    discus = ged.discus
                    session_date = ged.timestamp  # Время из базы записи
                    time_data = session_date.strftime("%Y-%m-%d"), session_date.strftime("%H.%M")
                    time_now = get_time()
                    difference = float(time_now[2]) - float(time_data[1]) # Difference
                    if time_data[0] == time_now[1] and difference < the_gap and discus is not None:
                        cache.append(discus)
                # Question to OpenAI
                cache.append(f"{message.text}\n")
                format_session_data = ' '.join(cache)

                # OpenAI
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
                    model_version = answer.model # Model
                    used_tokens = answer.usage.total_tokens 
                    # completion_tokens = chat_completion.usage.completion_tokens
                    # prompt_tokens = chat_completion.usage.prompt_tokens
                    ######### This date from Open AI ########
                    # flag_stik = False
                    stik = f"\n_{model_version}_\n_{used_tokens} ток._\n[/setup]" if flag_stik else ""
                    send = f"{text}\n\n{stik}"
                    await message.answer(send)


#                 # Push calcu..
#                 calculation(id, model_version, used_tokens, count_req_chat, money_user,\
#                             total_spent_money, used_token_chat) # Запуск функции статистики и возврат остатка денег на счете

                # Push update talking to DB
                cache.append(f"{text}\n")
                clear_data = ' '.join(cache)
                updated_data = {
                    "discus": clear_data,
                    # "timestamp": timestamp,
                    }
                await update_discussion(id, updated_data)
                cache = [] 


            else:
                await message.answer("Извините, но похоже, у вас нулевой баланс.\n Пополнить - [/setup]")
                logging.info(f"User {id} her money is finish.")
        else:
            await command_start_handler(message)
            logging.info(f"User {id} is not on DB, added.")
    else:
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
        except Exception as e:
            logging.error("Request timeout exceeded. Restart...")
            retries -= 1
            time.sleep(5)
        finally:
            pass












# async def main():
#     async_session = await create_async_engine_and_session()
#     async with async_session() as session:
#         # Do some asynchronous database operations here
#         pass


# async def main():
#     async_session = await create_async_engine_and_session()
#     async with async_session() as session:
#         # Пример чтения данных из базы данных Этот код выполняет запрос на выборку всех пользователей из таблицы User и выводит их имена.
#         result = await session.execute(select(UsersBase))
#         users = result.scalars().all()
#         for user in users:
#             print(user.name)


# await main(1)  # Здесь 1 - это id пользователя, которого вы хотите найти

# found_users = await main(1)  # Здесь 1 - это id пользователя, которого вы хотите найти
# if found_users:
#     for user in found_users:
#         # Делаете что-то с каждым найденным пользователем
# else:
#     print("Пользователь не найден.")





# from aiogram import Bot, Dispatcher, Router, types
# from aiogram.enums import ParseMode
# from aiogram.utils.markdown import hbold
# from aiogram.filters import CommandStart, Command
# from aiogram.types import Message
# from keys import token, api_key, white_list, admin_user_ids, block
# from worker_db import read_tele_user, add_update_tele_user, add_default_data, get_settings, update_talking, add_update_settings, admin_static_db, read_history_db
# from get_time import get_time
# from calculation import calculation

# from openai import AsyncOpenAI
# import asyncio
# import logging
# import time
# import sys


# client = AsyncOpenAI(api_key=api_key)
# TOKEN = token # Telegram
# dp = Dispatcher() # All handlers should be attached to the Router (or Dispatcher)
# bot = Bot(TOKEN, parse_mode="markdown") # Initialize Bot instance with a default parse mode which will be passed to all API calls



# # User_ID
# def user_id(action) -> int:
#     return action.from_user.id

# # Typing
# async def typing(action) -> None:
#     await bot.send_chat_action(action.chat.id, action='typing')



# # START Command("start")
# @dp.message(CommandStart())
# async def command_start_handler(message: Message) -> None:
#     await typing(message)
#     id = user_id(message)
#     ###
#     #full_name = message.from_user.full_name
#     name = message.from_user.username
#     first_name = message.from_user.first_name
#     last_name = message.from_user.last_name
#     chat = message.chat.id
#     is_user_admin = False
#     is_user_block = False
#     is_user_good = 3
#     ###
#     # Checking and added the parameters
#     if str(id) in admin_user_ids:
#         is_user_admin = True
#         logging.info(f"User id:{id} is admin added.")
#     if str(id) in block:
#         is_user_block=True
#         logging.info(f"User id:{id} is blocked added.")

#     # If this user is not in the database, we will add or update, because the user could get a block
#     add_update_tele_user(id=id, user_username=name, user_first_name=first_name, user_last_name=last_name,\
#     chat_id=chat, is_user_admin=is_user_admin , is_user_block=is_user_block , is_user_good=is_user_good) # abstractness
#     add_default_data(id) # Set default settings and text
#     logging.info(f"User id:{id} added in DB or not, if have added.")
    
#     # Choosing a name user
#     about = name if name else (first_name if first_name else (last_name if last_name else "bro"))

#     # Checking and added the parameters in Settings to white list users And gives them money
#     if str(id) in white_list:
#         money = 1000
#         add_update_settings(id, money_user=money) # Gives money
#         logging.info(f"User {about} received 1000 RUB")

#     logging.info(f"User {id} press /start")
#     await message.answer(f"Привет {about}! Я *ChatGPT*. Мне можно сразу задать вопрос или настроить - /setup.")



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


# # Message to OpenAI
# @dp.message()
# async def handle_message(message: types.Message):
#     id = user_id(message)
#     user_money = get_settings(id)
#     if message.text is not None and not message.text.startswith('/') and isinstance(message.text, str):
#         if user_money != (None, None):
#             if user_money[8] > 0 and user_money[8] != 0:
#                 await typing(message)

#                 cache = []
                
#                 ###### Data #######
#                 settings = get_settings(id)
#                 if settings is not None:
#                     model_chat = settings[7] # Модель из базы
#                     temp = settings[1] # Температура
#                     the_gap = settings[6] # Время хранения беседы
#                     count_req_chat = settings[3] # Всего вопросов заданных чату, для подсчетов ниже
#                     money_user = settings[8] # Деньги на счету  User money
#                     total_spent_money = settings[9] # Всего внесенно денег -  Total spending money
#                     used_token_chat = settings[4] # Всего использованно токенов за все время
#                 ####### Data #######

#                 read_history = read_history_db(id)
#                 if read_history:
#                     session_date = read_history[1] # Время из базы записи
#                     time_data = session_date.strftime("%Y-%m-%d"), session_date.strftime("%H.%M")
#                     time_now = get_time()
#                     difference = float(time_now[2]) - float(time_data[1]) # Difference
#                     if time_data[0] == time_now[1] and difference < the_gap and read_history[0] is not None:
#                         cache.append(read_history[0])
#                 # Question to OpenAI
#                 cache.append(f"{message.text}\n")
#                 format_session_data = ' '.join(cache)

#                 # OpenAI
#                 answer = await client.chat.completions.create(
#                     messages = [{"role": "user", "content": format_session_data,}],
#                     model = model_chat,
#                     temperature = temp,      # консервативность - разнообразие
#                     frequency_penalty = 0.5,  # 0 - допускает повторение слов и фраз в рамках данного ответа, 
#                     presence_penalty = 0.5, # 0 - допускает повторение слов и фраз из прошлых ответов
#                     #max_tokens=1000,
#                     )
                
#                 await typing(message)
#                 if answer != None:
#                     ######### This date from Open AI ########
#                     text = answer.choices[0].message.content # Text response AI
#                     model_version = answer.model # Model
#                     used_tokens = answer.usage.total_tokens 
#                     # completion_tokens = chat_completion.usage.completion_tokens
#                     # prompt_tokens = chat_completion.usage.prompt_tokens
#                     ######### This date from Open AI ########
#                     flag_stik = False
#                     stik = f"\n_{model_version}_\n_{used_tokens} ток._\n[/setup]" if flag_stik else ""
#                     send = f"{text}\n\n{stik}"
#                     await message.reply(send)
#                 logging.info(f"User {id} - {message.text}")


#                 # Push calcu..
#                 calculation(id, model_version, used_tokens, count_req_chat, money_user,\
#                             total_spent_money, used_token_chat) # Запуск функции статистики и возврат остатка денег на счете

#                 # Push update talking to DB
#                 cache.append(f"{text}\n")
#                 clear_data = ' '.join(cache)
#                 update_talking(id, clear_data)
#                 cache = [] 




#             else:
#                 await message.answer("Извините, но похоже, у вас нулевой баланс.\n Пополнить - [/setup]")
#                 logging.info(f"User {id} her money is finish.")
#         else:
#             await command_start_handler(message)
#             logging.info(f"User {id} is not on DB, added.")
#     else:
#         logging.error(f"Error, not correct message from User whose id is {id}")





























# # Main polling
# async def main() -> None:
#     await dp.start_polling(bot)

# # Start and Restart
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout) # При деплое закомментировать
#     #logging.basicConfig(level=logging.INFO, filename='log/app.log', filemode='a', format='%(levelname)s - %(asctime)s - %(name)s - %(message)s',) # При деплое активировать логирование в файл
#     retries = 5
#     while retries > 0:
#         try:
#             asyncio.run(main())
#         except Exception as e:
#             logging.error("Request timeout exceeded. Restart...")
#             retries -= 1
#             time.sleep(5)
#         finally:
#             pass










# # Temperature: Это параметр, который контролирует "консервативность" или "рискованность" ответов модели. При более высокой температуре модель будет более экспериментальной и неожиданной в своих ответах, иногда генерируя менее вероятные, но более креативные ответы. При низкой температуре модель будет более консервативной, предпочитая более вероятные, но менее разнообразные ответы. В вашем коде установлено значение 0.8, что означает умеренно высокую температуру.

# # Frequency Penalty: Этот параметр штрафует модель за генерацию тех же слов или фраз слишком часто в течение одного ответа. Увеличение этого значения приведет к более разнообразным ответам, так как модель будет стараться избегать повторений. В вашем коде установлено значение 0, что означает, что нет штрафа за частые повторения.

# # Presence Penalty: Этот параметр штрафует модель за включение некоторых слов или фраз, которые были использованы в предыдущих сообщениях чата. Увеличение этого значения побуждает модель к использованию более уникальных и разнообразных фраз. В вашем коде установлено значение 0.3, что указывает на умеренный штраф за повторы в предыдущих сообщениях.



#     # Most event objects have aliases for API methods that can be called in events' context
#     # For example if you want to answer to incoming message you can use `message.answer(...)` alias
#     # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
#     # method automatically or call API method directly via
#     # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`


# # @dp.message()
# # async def echo_handler(message: types.Message) -> None:
# #     """
# #     Handler will forward receive a message back to the sender

# #     By default, message handler will handle all message types (like a text, photo, sticker etc.)
# #     """
# #     try:
# #         # Send a copy of the received message
# #         await message.send_copy(chat_id=message.chat.id)
# #     except TypeError:
# #         # But not all the types is supported to be copied so need to handle it
# #         await message.answer("Nice try!")
        
#     # full_name = message.from_user.full_name
#     # name = message.from_user.username
#     # first_name = message.from_user.first_name
#     # last_name = message.from_user.last_name
#     # chat = message.chat.id