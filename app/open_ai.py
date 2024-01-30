from keys import api_key
from openai import AsyncOpenAI
import asyncio
from worker_db import update_talking, read_history_db, get_settings, add_update_settings
import datetime

client = AsyncOpenAI(api_key=api_key)

async def main(question: str, id: int):
    session_data = [] # Clearing the variable RAM
    # Get Settings
    settings = get_settings(id) # Get in DB all data settings ChatGPT
    model_chat = settings[7] # Model gpt
    the_gap = settings[6] # The storage time of the communication history
    total_used_token = settings[4] # Total tokens spent
    limit_token = settings[5] # Allowed Token Limit
    # The condition for using the communication history from the database
    read_history = read_history_db(id)
    if read_history:
        session_date = read_history[1] # Time of recording from the database
        time_data = session_date.strftime("%Y-%m-%d"), session_date.strftime("%H.%M") # Output the date and time in the Tuple
        date_time = datetime.datetime.utcnow() # Current date and time
        formatted_datetime = date_time.strftime("%Y-%m-%d"), date_time.strftime("%H.%M") # to Tuple
        difference = float(formatted_datetime[1]) - float(time_data[1]) # Difference
        if time_data[0] == formatted_datetime[0] and difference < the_gap and read_history[0] is not None: # The condition for using data from the database
            session_data.append(read_history[0]) # Adding a history to a variable

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
    # From the OpenAI response
    answer = chat_completion.choices[0].message.content # Text response AI
    model_version = chat_completion.model # Model
    # completion_tokens = chat_completion.usage.completion_tokens
    # prompt_tokens = chat_completion.usage.prompt_tokens
    total_tokens = chat_completion.usage.total_tokens 
    all_token = total_used_token + total_tokens # Всего токенов потрачено за все время
    limit_token = limit_token - all_token # Остаток лимита выданных токенов
    # All information in Tuples
    total_answer = answer, model_version, total_tokens, limit_token # Tuple
    # Push settings to DB
    add_update_settings(id, used_token_chat=all_token, limit_token_chat=limit_token) # Вносим изменения в настройки
    # Push update talking to DB
    session_data.append(f"{answer}\n") # Adding answer to a variable
    clear_data = ' '.join(session_data) # Put spaces and remove commas
    update_talking(id, clear_data) # Push variable talking to DB 
    session_data = [] # Clearing
    return total_answer or None

if __name__ == "__main__": # Если код запускается как основной файл (а не импортирован), тогда вызываем asyncio.run(main())
    asyncio.run(main())