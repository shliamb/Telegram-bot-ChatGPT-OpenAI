import sqlite3

# Функция для подключения к базе данных
def get_db_connection():
    database_path = './db/sqlite3.db'
    return sqlite3.connect(database_path)

# Данные для инициализации
initial_data_models_chat = [
    {'id': 1, 'models_chat': 'gpt-3.5-turbo'},
    {'id': 2, 'models_chat': 'gpt-4-1106-preview'},
    {'id': 3, 'models_chat': 'gpt-4'},
]

initial_data_patch_chat = [
    {'id': 1, 'patch_chat': 'Ответ не больше одного предложения'},
    {'id': 2, 'patch_chat': 'Ответ не больше 3 предложений'},
    {'id': 3, 'patch_chat': ' '},
]

# Вставка данных пользователя
def init_db_data_models_chat(id, models_chat):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO models_chat (id, models_chat) VALUES (?, ?)", (id, models_chat))
        conn.commit()

# Вставка данных пользователя patch_chat
def init_db_data_patch_chat(id, patch_chat):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO patch_chat (id, patch_chat) VALUES (?, ?)", (id, patch_chat))
        conn.commit()

# Запуск функции
for data in initial_data_models_chat:
    id=data['id']
    models_chat=data['models_chat']
    init_db_data_models_chat(id, models_chat)

# Запуск функции patch_chat
for data in initial_data_patch_chat:
    id=data['id']
    patch_chat=data['patch_chat']
    init_db_data_patch_chat(id, patch_chat)

