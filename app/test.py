# from keys import (
#     token, api_key, white_list, admin_user_ids, wallet_pay_token,
#     block, receiver_yoomoney, token_yoomoney)

# admin_id =  admin_user_ids[1:-1]

# # for admin_id in admin_user_ids:
# #     print(admin_id)



# print(admin_id)






class Form(StatesGroup):
    add_summ = State()
    confirm_summ = State()

@dp.callback_query(lambda c: c.data == 'pay_by_card')
async def start_invoice(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Введите сумму пополнения в RUB:", reply_markup=ReplyKeyboardRemove()) # !!!!
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(Form.add_summ)

@dp.message(Form.add_summ, F.content_type.in_({'text'}))
async def invoice_user(message: Message, state: FSMContext):
    
    mes_id = message.chat.id
    summ = message.text
    id = user_id(message)

    admin_id =  admin_user_ids[1:-1]
    url = f"tg://user?id={id}"
    await bot.send_message(admin_id, f" {summ} РУБ", parse_mode="HTML") # to admin message

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👛 Подтвердить", callback_data="confirm_summ_user")], 

        ]
    )
    await bot.send_message(admin_id, f"Пополнить счет на {summ}:", reply_markup=keyboard)
    await bot.send_message(message.chat.id, f"Ваш запрос принят, ожидайте пополнения.")

    #await state.update_data(summ=summ, id=id, admin_id=admin_id, mes_id=mes_id)

    await state.set_state(Form.confirm_summ)


@dp.callback_query(Form.confirm_summ, lambda c: c.data == 'confirm_summ_user')
async def process_add_money(callback_query: types.CallbackQuery, state: FSMContext):

    await bot.send_message("Привет")
    await state.clear()