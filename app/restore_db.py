from keys import pass_psgresql
import subprocess
import logging

db_username = "admin"
db_password = pass_psgresql
db_name = "my_database"
confirmation = False # На всякий случай подтверждение функции


def restore_db(file_path):

    terminate_command = f'PGPASSWORD={db_password} psql -h postgres -p 5432 -U {db_username} -d {db_name} -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname=\'{db_name}\';"'

    clear_command = f'PGPASSWORD={db_password} psql -h postgres -p 5432 -U {db_username} -d {db_name} -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"'

    pg_restore_command = f'PGPASSWORD={db_password} pg_restore -h postgres -p 5432 -U {db_username} -d {db_name} {file_path}'
    
    try:
        subprocess.run(terminate_command, shell=True) # Формирование команды для завершения активных сеансов

        subprocess.run(clear_command, shell=True) # Формирование команды для удаления базы данных

        subprocess.run(pg_restore_command, shell=True) # Восстановления базы данных из резервной копии с помощью pg_restore, выполнение команды через subprocess
        
        confirmation = True
        logging.info("Database restore completed successfully.")
    except Exception as e:
        confirmation = False
        logging.info(f"An error occurred: {e}")

    return confirmation


if __name__ == "__main__":
    restore_db()

#
# Очищает имеющуюся базу и восстанавливает из копии находящейся на сервере по адресу переданному по адресу и имени файла - file_path
# У меня чет на Linux pg_dump не обновляется выше 15.5, потому я поставил в docker-compose.yml
# версию 15.5 PostgreSQL, если на сервере будет выше, то в файле просто поставить Last img Postgres.
#
