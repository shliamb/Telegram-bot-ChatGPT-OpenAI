from forex_python.converter import CurrencyRates


# 1Febr2024 OpenAI:

# Model                         Input               Output

# gpt-4	                        $0.03 / 1K tokens	$0.06 / 1K tokens
# gpt-4-32k	                    $0.06 / 1K tokens	$0.12 / 1K tokens

# gpt-4-0125-preview	        $0.01 / 1K tokens	$0.03 / 1K tokens
# gpt-4-1106-preview	        $0.01 / 1K tokens	$0.03 / 1K tokens
# gpt-4-1106-vision-preview	    $0.01 / 1K tokens	$0.03 / 1K tokens

# gpt-3.5-turbo-1106	        $0.0010 / 1K tokens	$0.0020 / 1K tokens
# gpt-3.5-turbo-instruct	    $0.0015 / 1K tokens	$0.0020 / 1K tokens







def get_usd_to_rub_exchange_rate():
    # Создание объекта CurrencyRates
    c = CurrencyRates()

    # Получение курса рубля к доллару
    exchange_rate = c.get_rate('USD', 'RUB')

    return exchange_rate

# Получение курса рубля к доллару и вывод результата
usd_to_rub_rate = get_usd_to_rub_exchange_rate()
print(f"Курс рубля к доллару: {usd_to_rub_rate}")






# def usd_to_rub(amount_usd):
#     c = CurrencyRates() # Создание объекта CurrencyRates
#     exchange_rate = c.get_rate('USD', 'RUB') # Получение курса рубля к доллару
#     amount_rub = amount_usd * exchange_rate # Перевод суммы из долларов в рубли
#     return amount_rub

# # Пример использования функции
# amount_usd = 100  # Сумма в долларах
# amount_rub = usd_to_rub(amount_usd)
# print(f"{amount_usd} долларов равно {amount_rub} рублей")


price = {'gpt-3.5-turbo':0.006, 'gpt-4':0.18, 'gpt-4-1106-preview':0.08, 'gpt-4-32k':0.36} # $ / 1K tokens

#сравниваю с ценами на модели и высчитываю один токен


# def calculation(id, data_to_calculation):
#     id
#     ass = data_to_calculation[0]
#     tipe = data_to_calculation[1]


#     remaining_money = 1
#     return remaining_money
