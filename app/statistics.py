from worker_db import write_stat_db, add_update_settings

def save_ctatistics(id, model_version, used_tokens, value_1_tok_rub, rashod, all_countcount_req_chat, money_user,\
                    total_spent_money, used_token_chat): # Запуск функции статистики
    ###
    # Statistics
    write_stat_db(model=model_version, used_token=used_tokens, cost_token=value_1_tok_rub,\
                  entire_cost=rashod, users_telegram_id=id)
    ###
    # SettingsGPT
    all_token = used_token_chat + used_tokens
    all_count = all_countcount_req_chat + 1
    all_money = money_user - rashod
    total_spent_money = total_spent_money
    add_update_settings(id, used_token_chat=all_token, count_req_chat=all_count,\
                         money_user=all_money)#, total_spent_money=) - при пополнении баланса


    return