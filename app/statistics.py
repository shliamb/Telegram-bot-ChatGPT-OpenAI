import asyncio
from worker_db import add_statistic, update_settings

async def save_ctatistics(data): # Запуск функции статистики

    if data is not None:
        id = data['id']
        model_version = data['model_version']
        used_tokens = data['used_tokens']
        value_1_tok_rub = data['value_1_tok_rub']
        all_count_before = data['all_count']
        all_token_before = data['all_token']
        give_me_money = data['give_me_money']
        money = data['money']
        all_in_money = data['all_in_money']
        rashod = data['rashod']

    ###
    # Statistics
    new_data = {
        "use_model": model_version,
        "sesion_token": used_tokens,
        "price_1_tok": value_1_tok_rub,
        "price_sesion_tok": rashod,
        "users_telegram_id": id,
    }
    await add_statistic(new_data)

    ###
    # SettingsGPT
    all_token = all_token_before + used_tokens
    all_count = all_count_before + 1
    all_money = money - rashod
    # total_spent_money = total_spent_money # - при пополнении баланса

    updated_data = {
        "all_count": all_count,
        "all_token": all_token,
        "money": all_money,
    }
    await update_settings(id, updated_data)
 
    return


if __name__ == "__save_ctatistics__":
    asyncio.run(save_ctatistics())

