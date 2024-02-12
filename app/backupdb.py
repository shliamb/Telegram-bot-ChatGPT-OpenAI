from keys import pass_psgresql
import subprocess
import datetime
import logging

# Параметры подключения к базе данных PostgreSQL
db_username = "admin"
db_password = pass_psgresql
db_name = "my_database"

backup_path = "./backup_db/"

def backup_db():
    confirmation = False # Подтверждение

    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f'{db_name}_backup_{current_datetime}.sql'

    # Формирование команды для создания резервной копии с помощью pg_dump
    #pg_dump_command = f'PGPASSWORD={db_password} pg_dump -h localhost -p 5432 -U {db_username} -d {db_name} -f {backup_path}{backup_filename}'
    pg_dump_command = f'PGPASSWORD={db_password} pg_dump -h localhost -p 5432 -U {db_username} -d {db_name} -F c -f {backup_path}{backup_filename}' # В бинарный формат


    try:
        subprocess.run(pg_dump_command, shell=True) # Выполнение команды через subprocess
        confirmation = True
        logging.info("Backup Data Base is Completed.")

    except subprocess.CalledProcessError as e:
        confirmation = False
        logging.error(f"Error when creating a backup: {e}")
    return confirmation


if __name__ == "__main__":
    backup_db()

#
# У меня чет на Linux pg_dump не обновляется выше 15.5, потому я поставил в docker-compose.yml
# версию 15.5 PostgreSQL, если на сервере будет выше, то в файле просто поставить Last img Postgres.
#
