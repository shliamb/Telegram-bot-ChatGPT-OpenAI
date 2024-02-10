from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types





# MENU
#main
async def main_menu(bot, message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Настройки", callback_data="sub_setings")], 
            [InlineKeyboardButton(text="Сброс диалога", callback_data="sub_dialog")],
            [InlineKeyboardButton(text="Финансы", callback_data="sub_balance")], 
            [InlineKeyboardButton(text="О боте", callback_data="sub_about")],
            [InlineKeyboardButton(text="Закрыть меню X", callback_data="close")]
        ]
    )
    await message.answer("Выберите действие:", reply_markup=keyboard)

# Back to main
async def back_to_main(bot, callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Настройки", callback_data="sub_setings")], 
            [InlineKeyboardButton(text="Сброс диалога", callback_data="sub_dialog")],
            [InlineKeyboardButton(text="Финансы", callback_data="sub_balance")], 
            [InlineKeyboardButton(text="О боте", callback_data="sub_about")],
            [InlineKeyboardButton(text="Закрыть меню X", callback_data="close")]
        ]
    )
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                         message_id=callback_query.message.message_id,
                                         reply_markup=keyboard)

#### SETTINGS ####
# Settings - main
async def sub_setings(bot, callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                [InlineKeyboardButton(text="Модель ChatGPT", callback_data="model")],
                [InlineKeyboardButton(text="Время хранения диалога", callback_data="time")],
                [InlineKeyboardButton(text="Креативность", callback_data="creativ")],
                [InlineKeyboardButton(text="Повторения в ответе", callback_data="repet")],
                [InlineKeyboardButton(text="Повторения в ответах", callback_data="repet_all")],
                [InlineKeyboardButton(text="Вкл/Отл статистику в ответ", callback_data="flag_stik")],
                [InlineKeyboardButton(text="Вернуться назад", callback_data="back_to_main")],
        ]
    )
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=keyboard)

# Settings - back to main
async def back_to_setings(bot, callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                [InlineKeyboardButton(text="Модель", callback_data="model")],
                [InlineKeyboardButton(text="Время хранения диалога", callback_data="time")],
                [InlineKeyboardButton(text="Креативность", callback_data="creativ")],
                [InlineKeyboardButton(text="Повторения в ответе", callback_data="repet")],
                [InlineKeyboardButton(text="Повторения в прош. ответах", callback_data="repet_all")],
                [InlineKeyboardButton(text="Вкл/Отл статистику в ответ", callback_data="flag_stik")],
                [InlineKeyboardButton(text="Вернуться назад", callback_data="back_to_main")],
        ]
    )
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                         message_id=callback_query.message.message_id,
                                         reply_markup=keyboard)

# Sub menu Settings - Model
async def sub_setings_model(bot, callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                #[InlineKeyboardButton(text="gpt-4-0613", callback_data="gpt-4-0613")],
                [InlineKeyboardButton(text="gpt-4-1106-preview", callback_data="gpt-4-1106-preview")],
                [InlineKeyboardButton(text="gpt-4-0125-preview", callback_data="gpt-4-0125-preview")],
                [InlineKeyboardButton(text="gpt-3.5-turbo-0613", callback_data="gpt-3.5-turbo-0613")],
                [InlineKeyboardButton(text="Вернуться назад", callback_data="back_to_setings")],
        ]
    )
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=keyboard)

# Sub menu Settings - Time
async def sub_setings_time(bot, callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                [InlineKeyboardButton(text="Не запоминать", callback_data="no_time")],
                [InlineKeyboardButton(text="5 минут", callback_data="5_time")],
                [InlineKeyboardButton(text="15 минут", callback_data="15_time")],
                [InlineKeyboardButton(text="30 минут", callback_data="30_time")],
                [InlineKeyboardButton(text="Вернуться назад", callback_data="back_to_setings")],
        ]
    )
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=keyboard)

# Sub menu Settings - Creativ
async def sub_setings_creativ(bot, callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                [InlineKeyboardButton(text="100% Консервативность", callback_data="creativ_0")],
                [InlineKeyboardButton(text=f"70% - 30%", callback_data="creativ_3")],
                [InlineKeyboardButton(text=f"50% - 50%", callback_data="creativ_5")],
                [InlineKeyboardButton(text=f"30% - 70%", callback_data="creativ_7")],
                [InlineKeyboardButton(text="Разнообразие 100%", callback_data="creativ_1")],
                [InlineKeyboardButton(text="Вернуться назад", callback_data="back_to_setings")],
        ]
    )
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=keyboard)
    
# Sub menu Settings - repet
async def sub_setings_repet(bot, callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                [InlineKeyboardButton(text="0% Повторения в ответе", callback_data="repet_0")],
                [InlineKeyboardButton(text=f"30%", callback_data="repet_3")],
                [InlineKeyboardButton(text=f"50%", callback_data="repet_5")],
                [InlineKeyboardButton(text=f"70%", callback_data="repet_7")],
                [InlineKeyboardButton(text="Повторения в ответе 100%", callback_data="repet_1")],
                [InlineKeyboardButton(text="Вернуться назад", callback_data="back_to_setings")],
        ]
    )
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=keyboard)

# Sub menu Settings - repet_all
async def sub_setings_repet_all(bot, callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                [InlineKeyboardButton(text="0% Повторения в ответах", callback_data="repet_all_0")],
                [InlineKeyboardButton(text=f"30%", callback_data="repet_all_3")],
                [InlineKeyboardButton(text=f"50%", callback_data="repet_all_5")],
                [InlineKeyboardButton(text=f"70%", callback_data="repet_all_7")],
                [InlineKeyboardButton(text="Повторения в ответах 100%", callback_data="repet_all_1")],
                [InlineKeyboardButton(text="Вернуться назад", callback_data="back_to_setings")],
        ]
    )
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=keyboard)




async def sub_balance(bot, callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                [InlineKeyboardButton(text="Баланс", callback_data="my_many")],
                [InlineKeyboardButton(text="Пополнить баланс", callback_data="add_money")],
                [InlineKeyboardButton(text="Статистика 100 пос.", callback_data="statis_30")],
                [InlineKeyboardButton(text="Вернуться назад", callback_data="back_to_main")],
        ]
    )
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                         message_id=callback_query.message.message_id,
                                         reply_markup=keyboard)



async def sub_add_money(bot, callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
                [InlineKeyboardButton(text="100 RUB", callback_data="many_100")],
                [InlineKeyboardButton(text="200 RUB", callback_data="many_200")],
                [InlineKeyboardButton(text="500 RUB", callback_data="many_500")],
                [InlineKeyboardButton(text="700 RUB", callback_data="many_700")],
                [InlineKeyboardButton(text="1000 RUB", callback_data="many_1000")],
                [InlineKeyboardButton(text="2000 RUB", callback_data="many_2000")],
                [InlineKeyboardButton(text="Вернуться назад", callback_data="back_to_main")],
        ]
    )
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                         message_id=callback_query.message.message_id,
                                         reply_markup=keyboard)






async def admin_menu(bot, message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Скачать статистику", callback_data="admin_stat")], 
            [InlineKeyboardButton(text="Скачать логи", callback_data="admin_get_log")],
            [InlineKeyboardButton(text="Очистить логи", callback_data="admin_clear_log")], 
            [InlineKeyboardButton(text="Подтвердить оплату переводом", callback_data="confirm_pay")],
            [InlineKeyboardButton(text="Закрыть меню X", callback_data="close_admin")]
        ]
    )
    await message.answer("Выберите действие:", reply_markup=keyboard)





# async def sub_dialog(bot, callback_query: types.CallbackQuery):
#     keyboard = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text="Вернуться назад", callback_data="back_to_main")
#             ]
#         ]
#     )
#     await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
#                                          message_id=callback_query.message.message_id,
#                                          reply_markup=keyboard)



# async def sub_about(bot, callback_query: types.CallbackQuery):
#     keyboard = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text="Вернуться назад", callback_data="back_to_main")
#             ]
#         ]
#     )
#     await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
#                                          message_id=callback_query.message.message_id,
#                                          reply_markup=keyboard)




