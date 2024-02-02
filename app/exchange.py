import xml.etree.ElementTree as ET # Pars XML
from urllib.request import urlopen
from worker_db import get_exchange, write_exchange
from get_time import get_time

# Get exchange USD to RUB - переводит из доллара в рубли через XML Центробанка, так как все зарубежные не предоставляют о RUB, я не нашел бесплатно


# Получение стоимости 1$ 
def exchange():
    try:
        usd = 1 # 1$ to RUB
        with urlopen("https://www.cbr.ru/scripts/XML_daily.asp", timeout=10) as data: # 10 секунд ожидание ответа от ресурса дальше таймоут
            ex = (ET.parse(data).findtext('.//Valute[@ID="R01235"]/Value')) # значения валюты доллара США (USD) с помощью XPath выражения 
        ex = ex.replace(',', '.')  # Замена запятой на точку
        rub = float(usd) * float(ex)
        rub = round(rub, 2) # Округление до 2 цифр после запятой
    except:
        print("Ошибка при получении курса валюты от сервера центрабанка РФ, курс останется на последнем обновлении.")
        rub = None
    return rub or None  # Возврат стоимости одного $


# Получение из DB курса, если старее 1 дня, то обновляем
def usd_to_rub():
    get_exchange_db = get_exchange() # Забераем запись курса доллара из базы
    if get_exchange_db != (None, None):# Если запись в базе курса доллара есть
        # Date record in DB
        date_time_db = get_exchange_db[0] # Дата и время из базы
        date_db = date_time_db.strftime("%Y-%m-%d") # Только дата из DB
        # Date now
        time_now = get_time() # Время и дата сейчас
        data_now = time_now[1] # Только дата сейчас
        data_now_all = time_now[0] # Дата и время сейчас полностью
        rub = get_exchange_db[1] # Курс из базы

        if date_db != data_now:
            rub_now = exchange()

            if rub_now != None:
                rub = rub_now
                write_exchange(timestamp=data_now_all, price=rub)

    else:
        rub_now = exchange()

        if rub_now != None:
            rub = rub_now
            write_exchange(price=rub)
        else:
            rub = 100 # Если и в базе нет и центробанк сдох, то вот так, сорян.. думаю меньше ему не быть в остатке моей жизни

    return rub


if __name__ == "__main__":
    usd_to_rub()
















