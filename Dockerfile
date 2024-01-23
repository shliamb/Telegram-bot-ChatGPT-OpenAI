# Используйте официальный образ Python
FROM python:3.8

# Установите рабочий каталог в контейнере
WORKDIR /usr/src/app

# Копируйте файлы зависимостей и устанавливаем их
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируйте исходный код вашего бота в контейнер
COPY . .

# Запускайте бота при старте контейнера
CMD [ "python", "./telegram-bot.py" ]