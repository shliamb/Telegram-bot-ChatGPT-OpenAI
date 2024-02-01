from worker_db import get_settings, add_update_settings


# Получаем из базы
# settings = get_settings(id)  - получаем с базы статистику
# all_money_spend = settings[9] # Total spending money - вносимые суммы за все время получаем
# money = settings[8]   - наличие на счету, может быть минус, нужно учесть


# оплата  сумма


# Вносим в базу
# new_money = money + сумма
# add_update_settings(all_money_spend=сумма, money_user=new_money) - добавляем в базу при оплате суммы