# init SQLite3 db
import sqlite3

# Путь к файлу базы данных
database_path = '/sqlite3.db'

def create_tables():
    # Подключение к базе данных
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Создание таблицы
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS my_table (
            id INTEGER PRIMARY KEY,
            column1 TEXT,
            column2 INTEGER
        )
    ''')

    # Закрытие соединения с базой данных
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Таблицы успешно созданы.")