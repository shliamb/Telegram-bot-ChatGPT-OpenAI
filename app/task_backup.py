import schedule
from backupdb import backup_db
import logging

def my_task():
    backup_db() # Бэкап базы данных
    logging.info(f"Task to Backup Data Base is run.")

schedule.every().day.at("02:05").do(my_task)
#schedule.every(24).hours.do(my_task)


if __name__ == "__main__":
    my_task()


# Автоматический запуск таски, а она запускает бекап
#
#    
#
# schedule.every(1).minutes.do(my_task)
# schedule.every(10).minutes.do(task1)
# schedule.every(2).hours.do(task2)
# schedule.every().monday.at("12:00").do(task1)
# schedule.every().wednesday.at("14:00").do(task2)