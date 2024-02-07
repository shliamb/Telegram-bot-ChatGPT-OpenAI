import datetime # not support async
import logging

def get_time():
    try:
        all_date = datetime.datetime.utcnow()
        day = all_date.strftime("%Y-%m-%d")
        time = all_date.strftime("%H.%M")
        send = {"day": day, "time": time, "all_date": all_date}
        logging.info(f"Current date and time geted.")
        return send
    except Exception as e:
        logging.error(f"Error get current date and time: {e}")

if __name__ == "__get_time__":
    get_time()