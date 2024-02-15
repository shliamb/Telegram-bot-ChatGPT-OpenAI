
# Используйте базовый образ Python
FROM python:3.12-slim

# Установите переменную окружения PYTHONUNBUFFERED=1
ENV PYTHONUNBUFFERED=1

# Установка PostgreSQL
RUN apt-get update && apt-get install -y postgresql postgresql-contrib

# Установка утилиты pg_dump
RUN apt-get install -y postgresql-client

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# Скопируйте все файлы из текущего каталога в контейнер
COPY . .

# Определите команду для запуска вашего приложения
CMD ["python", "app/run_bot.py"]
