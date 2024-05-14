FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

# Установка apt-utils
RUN apt-get update && apt-get install -y apt-utils

# Установка PostgreSQL и утилиты pg_dump
RUN apt-get update && apt-get install -y \
    postgresql \
    postgresql-contrib \
    postgresql-client

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app/run_bot.py"]
