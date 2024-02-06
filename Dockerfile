FROM  python:3.12-slim 

WORKDIR /app

COPY . .

# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r ./requirements.txt

#COPY . .

#CMD [ "python", "./app/run_bot.py" ]


# FROM python:3.8-slim

# #WORKDIR /app

# COPY . .

# #RUN pip install --upgrade pip -- only first time

# RUN pip install -r requirements.txt

CMD ["python", "app.py"]
