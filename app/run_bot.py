# Run telegram bot ChatGPT
import time
import requests
from logging_bot import logger

while True:
    try:
        pass
        print("Погнали...")
        from tele_bot import start_bot
        start_bot(none_stop=True, timeout=60)
        break
    except requests.exceptions.ReadTimeout:
        logger.error("Request timeout exceeded. Restart...")
        print("Request timeout exceeded. Restart...")
        time.sleep(5)
    # except Exception as e:
    #     logger.exception("Произошла непредвиденная ошибка:")
    #     print(f"Error : {e}")
    #     break
