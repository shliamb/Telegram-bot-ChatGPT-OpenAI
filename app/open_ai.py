from keys import api_key
from openai import AsyncOpenAI
import asyncio
from worker_db import update_talking, read_history_db, get_settings, add_update_settings
from get_time import get_time
from calculation import calculation

client = AsyncOpenAI(api_key=api_key)

async def main(question: str, id: int):
    session_data = [] # Clearing the variable RAM

    ###### Data #######
    settings = get_settings(id) # Get in DB all data settings ChatGPT
    if settings is not None:
        model_chat = settings[7] # Модель -  Model gpt - модель
        the_gap = settings[6] # Время хранения - The storage time of the communication history - время хранения
        count_req_chat = settings[3] # Total count request - всего вопросов заданных чату, для подсчетов ниже
        money_user = settings[8] # Деньги на счету  User money
        total_spent_money = settings[9] # Всего внесенно денег -  Total spending money
        used_token_chat = settings[4] # Всего использованно токенов за все время
    ####### Data #######

    read_history = read_history_db(id)
    if read_history:
        session_date = read_history[1] # Time of recording from the database
        time_data = session_date.strftime("%Y-%m-%d"), session_date.strftime("%H.%M") # Output the date and time in the Tuple
        time_now = get_time()
        difference = float(time_now[2]) - float(time_data[1]) # Difference
        if time_data[0] == time_now[1] and difference < the_gap and read_history[0] is not None: # The condition for using data from the database
            session_data.append(read_history[0]) # Adding a history to a variable
    # Question to OpenAI
    session_data.append(f"{question}\n") # Adding new question to a variable
    format_session_data = ' '.join(session_data) # We put spaces and remove commas
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

    if chat_completion:
        ######### This date from Open AI ########
        answer = chat_completion.choices[0].message.content # Text response AI
        model_version = chat_completion.model # Model
        used_tokens = chat_completion.usage.total_tokens 
        # completion_tokens = chat_completion.usage.completion_tokens
        # prompt_tokens = chat_completion.usage.prompt_tokens
        ######### This date from Open AI ########

        calculation(id, model_version, used_tokens, count_req_chat, money_user,\
                     total_spent_money, used_token_chat) # Запуск функции статистики и возврат остатка денег на счете

        # All information to Tuples
        total_answer = answer, model_version, used_tokens # Tuple all answer - Кортэж для ответа чата на вопрос

    # Push update talking to DB
    session_data.append(f"{answer}\n") # Adding answer to a variable
    clear_data = ' '.join(session_data) # Put spaces and remove commas
    update_talking(id, clear_data) # Push variable talking to DB 
    session_data = [] # Clearing
    return total_answer or None

if __name__ == "__main__": # Если код запускается как основной файл (а не импортирован), тогда вызываем asyncio.run(main())
    asyncio.run(main())