# 1Febr2024 OpenAI:

# Model                         Input               Output

# gpt-4	                        $0.03 / 1K tokens	$0.06 / 1K tokens
# gpt-4-32k	                    $0.06 / 1K tokens	$0.12 / 1K tokens

# gpt-4-0125-preview	        $0.01 / 1K tokens	$0.03 / 1K tokens
# gpt-4-1106-preview	        $0.01 / 1K tokens	$0.03 / 1K tokens
# gpt-4-1106-vision-preview	    $0.01 / 1K tokens	$0.03 / 1K tokens

# gpt-3.5-turbo-1106	        $0.0010 / 1K tokens	$0.0020 / 1K tokens
# gpt-3.5-turbo-instruct	    $0.0015 / 1K tokens	$0.0020 / 1K tokens

import xml.etree.ElementTree as ET # Pars XML
from urllib.request import urlopen

price = {                      # if 1$ - 90.23:
    "gpt-3.5-turbo":0.006,     # 0.54 руб 
    "gpt-4":0.18,              # 16.24 руб
    "gpt-4-1106-preview":0.08, # 7.22 руб 
    "gpt-4-32k":0.36,          # 32.48  руб
    }


# Get exchange USD to RUB - переводит из доллара в рубли через XML Центробанка, так как все зарубежные не предоставляют о RUB, я не нашел бесплатно
def usd_to_rub(usd):
    with urlopen("https://www.cbr.ru/scripts/XML_daily.asp", timeout=10) as data: # 10 секунд ожидание ответа от ресурса дальше таймоут
        ex = (ET.parse(data).findtext('.//Valute[@ID="R01235"]/Value')) # значения валюты доллара США (USD) с помощью XPath выражения 
    ex = ex.replace(',', '.')  # Замена запятой на точку
    rub = float(usd) * float(ex)
    rub = round(rub, 2) # Округление
    return rub


def calculation(id, data):
    model = data[0]
    used_tokens = data[1]

    for key, value in price.items():
        if key == model:
            value_1_tok = value / 1000 # Price 1 token to USD
            used_tok_usd = used_tokens * value_1_tok # Price data to USD
            used_tok_rub = usd_to_rub(used_tok_usd)
            return used_tok_rub



id = 2
data = "gpt-4", 1000
ass = calculation(id, data)
print(ass)



#сравниваю с ценами на модели и высчитываю один токен


# def calculation(id, data_to_calculation):
#     id
#     ass = data_to_calculation[0]
#     tipe = data_to_calculation[1]


#     remaining_money = 1
#     return remaining_money
