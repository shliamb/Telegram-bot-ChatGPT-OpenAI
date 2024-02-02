import datetime

def get_time():
    date_time = datetime.datetime.utcnow() # Current date and time
    date = date_time.strftime("%Y-%m-%d") # Only date 
    time = date_time.strftime("%H.%M") # Only time
    return date_time, date, time # in Tuple