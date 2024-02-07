import asyncio
import aiohttp
import xml.etree.ElementTree as ET # Pars XML
import logging
from worker_db import get_exchange, update_exchange, add_exchange
from get_time import get_time

# Get exchange USD to RUB - переводит из доллара в рубли через XML Центробанка, так как все зарубежные не предоставляют о RUB, я не нашел бесплатно


# Получение стоимости 1$ 
async def exchange():
    try:
        usd = 1 # 1$ to RUB
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.cbr.ru/scripts/XML_daily.asp", timeout=10) as response:
                data = await response.text()
        ex = (ET.fromstring(data).findtext('.//Valute[@ID="R01235"]/Value')) # значения валюты доллара США (USD) с помощью XPath выражения 
        ex = ex.replace(',', '.')  # Замена запятой на точку
        rub = float(usd) * float(ex)
        rub = round(rub, 2) # Округление до 2 цифр после запятой
        logging.info(f"Geting ex rate 1$ - {rub} Centrobank")
    except Exception as e:
        logging.error(f"Error geting exchange rate to url Centrobank")
        rub = None
    return rub or None  # Возврат стоимости одного $



# Получение из DB курса, если старее 1 дня, то обновляем
async def usd_to_rub():
    get_exchange_db = await get_exchange() # Забераем запись курса доллара из базы
    if get_exchange_db is not None:# Если запись в базе курса доллара есть
        # Date record in DB
        rub = get_exchange_db.rate
        date_time_db = get_exchange_db.timestamp
        date_db = date_time_db.strftime("%Y-%m-%d") # Только дата из DB
        # Date now
        now = get_time()
        if now is not None:
            date_now = now['day']
            all_date = now['all_date']
        else:
            return rub
        if date_db != date_now:
            rub_now = await exchange()
            if rub_now is not None:
                rub = rub_now
                id = 1
                data = {"rate": rub, "timestamp": all_date}
                await update_exchange(id, data)
        else:
            logging.info(f"Exchange rate is remained the same")

    else:
        rub_now = await exchange()
        if rub_now is not None:
            rub = rub_now
            data = {"id": 1, "rate": rub,}
            await add_exchange(data)
        else:
            rub = 100 # Если и в базе нет и центробанк сдох, то вот так, сорян.. думаю меньше ему не быть в остатке моей жизни
            logging.error(f"Exchange rate is 100 RUB. Update is not worcking.")
    
    return rub



if __name__ == "__usd_to_rub__":
    asyncio.get(usd_to_rub())












