import xml.etree.ElementTree as ET # Pars XML
from urllib.request import urlopen

# Get rate USD - RUB
def get_exchange(usd):
    with urlopen("https://www.cbr.ru/scripts/XML_daily.asp", timeout=10) as data: # 10 секунд ожидание ответа от ресурса дальше таймоут
        ex = (ET.parse(data).findtext('.//Valute[@ID="R01235"]/Value')) # значения валюты доллара США (USD) с помощью XPath выражения 
    ex = ex.replace(',', '.')  # Замена запятой на точку
    rub = float(usd) * float(ex)
    rub = round(rub, 2) # Округление
    return rub




usd = 1
ass = get_exchange(usd)
print(ass)

# if __name__ == "__main__":
#     print(get_rate())