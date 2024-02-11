from keys import pass_psgresql
import subprocess
import datetime
import logging

# Параметры подключения к базе данных PostgreSQL
db_username = "admin"
db_password = pass_psgresql
db_name = "my_database"
confirmation = False

backup_path = "./backup_db/"
backup_filename = "my_database_backup_2024-02-11_11-21-10.sql"  # Имя вашего файла резервной копии

def restore_db():

    # Очистка базы данных перед восстановлением
    clear_command = f'PGPASSWORD={db_password} psql -h localhost -p 5432 -U {db_username} -d {db_name} -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"'


    # Восстановление базы
    pg_restore_command = f'PGPASSWORD={db_password} pg_restore -h localhost -p 5432 -U {db_username} -d {db_name} {backup_path}{backup_filename}'
    
    try:
        subprocess.run(clear_command, shell=True)
        # Восстановление базы данных
        subprocess.run(pg_restore_command, shell=True) # Выполнение команды через subprocess
        
        confirmation = True
        print("Database restore completed successfully.")
    except Exception as e:
        confirmation = False
        print(f"An error occurred: {e}")

    return confirmation



if __name__ == "__main__":
    restore_db()


# У меня чет на Linux pg_dump не обновляется выше 15.5, потому я поставил в docker-compose.yml
# версию 15.5 PostgreSQL, если на сервере будет выше, то в файле просто поставить Last img Postgres.
#
#
#
#
#
# async def restore_database():
#     # Закрыть текущую сессию и хранилище данных
#     await bot.session.close()
#     await dp.storage.close()

#     # Выполнить операцию восстановления из копии базы данных
#     # Ваш код для восстановления из копии базы данных здесь

# # Затем вызовите функцию восстановления
# await restore_database()