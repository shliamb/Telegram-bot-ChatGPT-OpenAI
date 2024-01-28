from keys import api_key
from openai import AsyncOpenAI
import asyncio
# from typing import Union
from worker_db import add_session_data, read_data_ans_ques, get_settings, update_settings
import datetime


client = AsyncOpenAI(api_key=api_key)



async def main(question: str, id: int): # -> Union[str, None]:
    session_data = [] # Clear переменную ОЗУ каждый раз на всякий случай
    # Получаю из DB model_chat и the_gap по id
    settings = get_settings(id)
    model_chat = settings[7] # Модель
    the_gap = settings[6] # Часы.минуты время использования истории общения
    total_used_token = settings[4] # Всего использованно токенов
    limit_token = settings[5] # Выданный лимит токенов
    # Условие вычитывания истории вопросов-ответа, наверно проверяется время обновления времени последней записи, если больше часа, то или очищает, то ли другую ячейку..
    read_data = read_data_ans_ques(id)
    if read_data:
        session_date = read_data[1] # Дата и время переписки из DB
        time_data = session_date.strftime("%Y-%m-%d"), session_date.strftime("%H.%M") # Вывод в кортеже
        date_time = datetime.datetime.utcnow() # Получаем текущую дату и время
        formatted_datetime = date_time.strftime("%Y-%m-%d"), date_time.strftime("%H.%M")
        difference = float(formatted_datetime[1]) - float(time_data[1])
        if time_data[0] == formatted_datetime[0] and difference < the_gap and read_data[0] is not None: # Условие использование данных из базы
            session_data.append(read_data[0]) # Добавляем к переменной историю из DB

    #raise



    session_data.append(f"{question}\n") # Добавляю новый вопрос в переменную ОЗУ
    format_session_data = ' '.join(session_data) # Пробелы между словами и убираю запятую

    #raise
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": format_session_data,
            }
        ],
        model=model_chat,
    )

    answer = chat_completion.choices[0].message.content # Ответ
    model_version = chat_completion.model
    completion_tokens = chat_completion.usage.completion_tokens
    prompt_tokens = chat_completion.usage.prompt_tokens
    total_tokens = chat_completion.usage.total_tokens
    all_token = total_used_token + total_tokens # Всего токенов потрачено за все время
    limit_token = limit_token - all_token # Остаток лимита выданных токенов
    total_answer = answer, model_version, completion_tokens, prompt_tokens, total_tokens, all_token, limit_token # В кортеж
    session_data.append(f"{answer}\n") # Добавляю ответ
    clear_data = ' '.join(session_data) # Пробелы между словами и убираю запятую
    # Передаю переменую ОЗУ в DB переписывая ячейку по id
    #raise
    add_session_data(id, clear_data) # Вношу данные из переменной в DB, дата меняется автоматом
    session_data = [] # Чистим переменную
    update_settings(id, all_token, limit_token) # Вносим изменения в настройки
    return total_answer or None # Возвращаю ответ
if __name__ == "__main__": # Если код запускается как основной файл (а не импортирован), тогда вызываем asyncio.run(main())
    asyncio.run(main())







