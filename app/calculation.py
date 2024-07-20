import asyncio
from exchange import usd_to_rub
from statistics import save_ctatistics

# Прайс моделей и цен на них за 1000 токенов

price = {                              # if 1$ - 100 RUB:
    'gpt-3.5-turbo-0613': 0.006,       # 0.54 RUB  
    'gpt-4-0613': 0.18,                # 16.24 RUB
    'gpt-4-1106-preview': 0.08,        # 7.22 RUB 
    'gpt-4-32k': 0.36,                 # 32.48 RUB     но к ней нет доступа !!!
    'gpt-4-0125-preview': 0.08,        # 7.22 RUB      GPT-4 Turbo
    'gpt-4o-2024-05-13': 0.04,         # 4 RUB         GPT-4o

    'gpt-4o-mini-2024-07-18': 0.0015,  # 0.15 RUB      GPT-4o-mini супер новая
    'gpt-3.5-turbo-0125': 0.004,       # 0.4 RUB       16K context window and is optimized for dialog
    'gpt-3.5-turbo-instruct': 0.005,   # 0.5 RUB       model supports a 4K context window  не пашет чет...
    }


# Калькуляция расхода и запись в базу
async def calculation(data):
    if data is not None:
        id = data['id']
        model_version = data['model_version']
        used_tokens = data['used_tokens']
        all_count = data['all_count']
        all_token = data['all_token']
        give_me_money = data['give_me_money']
        money = data['money']
        all_in_money = data['all_in_money']



    curs = await usd_to_rub()
    value_1_tok_rub = None

    for key, value in price.items():
        if key == model_version:
            value_1_tok_usd = value / 1000 # Price 1 token to USD
            value_1_tok_rub = value_1_tok_usd * curs # Price 1 token to RUB
    if value_1_tok_rub == None:
        print(f"В прайсе не найдена {model_version} модель, обновите прайс в calculation.py")
        # Log
        value_1_tok_rub = 0.03248
    rashod = value_1_tok_rub * used_tokens # Расход

    data = {
        "id": id,
        "model_version": model_version,
        "used_tokens": used_tokens,
        "value_1_tok_rub": value_1_tok_rub,
        "all_count": all_count,
        "all_token": all_token,
        "give_me_money": give_me_money,
        "money": money,
        "all_in_money": all_in_money,
        "rashod": rashod,
    }

    await save_ctatistics(data) # Запуск функции статистики

    return rashod

if __name__ == "__main__":
    asyncio.run(calculation())


# 1Jul2024 OpenAI:

# Model                         Input               Output

# gpt-4	                        $0.03 / 1K tokens	$0.06 / 1K tokens
# gpt-4-32k	                    $0.06 / 1K tokens	$0.12 / 1K tokens

# gpt-4-0125-preview	        $0.01 / 1K tokens	$0.03 / 1K tokens
# gpt-4-1106-preview	        $0.01 / 1K tokens	$0.03 / 1K tokens
# gpt-4-1106-vision-preview	    $0.01 / 1K tokens	$0.03 / 1K tokens

# gpt-3.5-turbo-1106	        $0.0010 / 1K tokens	$0.0020 / 1K tokens
# gpt-3.5-turbo-instruct	    $0.0015 / 1K tokens	$0.0020 / 1K tokens

# gpt-4o-2024-05-13             $0.02

# gpt-4o-mini-2024-07-18        $0.00075
# gpt-3.5-turbo-0125            $0.002
# gpt-3.5-turbo-instruct        $0.0025 