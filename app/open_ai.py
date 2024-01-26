from keys import api_key
from openai import AsyncOpenAI
import asyncio
from typing import Union


client = AsyncOpenAI(api_key=api_key)

all_in = []

async def main(question: str) -> Union[str, None]:

    # Добавляю вопросы в кучу для поддержания контекста
    all_in.append(f"{question}\n") # Добавляю вопрос
    res = ' '.join(all_in) # Пробелы между словами и убираю запятую
    print(res)


    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": res, #question,
            }
        ],
        model="gpt-3.5-turbo", #"gpt-4", "text-davinci-002", "text-curie-003", or "gpt-3.5-turbo"
    )

    answer = chat_completion.choices[0].message.content # Ответ
    model_version = chat_completion.model
    completion_tokens = chat_completion.usage.completion_tokens
    prompt_tokens = chat_completion.usage.prompt_tokens
    total_tokens = chat_completion.usage.total_tokens
    total_answer = answer, model_version, completion_tokens, prompt_tokens, total_tokens # В кортеж
    #print(f"Ответ {answer}\nВерсия модели {model_version}\nЗавершенные токены {completion_tokens}\nПодсказки_токены {prompt_tokens}\nВсего токенов {total_tokens} ")
    # print(total_answer[0])
    all_in.append(f"{answer}\n") # Добавляю вопрос


    return total_answer or None

if __name__ == "__main__": # Если код запускается как основной файл (а не импортирован), тогда вызываем asyncio.run(main())
    asyncio.run(main())






# async def main(question) -> None:
#     chat_completion = await client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": question,
#             }
#         ],
#         model="gpt-3.5-turbo",
#     )
#     answer = chat_completion.choices[0].message.content # Ответ
#     model_version = chat_completion.model
#     completion_tokens = chat_completion.usage.completion_tokens
#     prompt_tokens = chat_completion.usage.prompt_tokens
#     total_tokens = chat_completion.usage.total_tokens
#     total_answer = answer, model_version, completion_tokens, prompt_tokens, total_tokens # В кортеж
#     print(f"Ответ {answer}\nВерсия модели {model_version}\nЗавершенные токены {completion_tokens}\nПодсказки_токены {prompt_tokens}\nВсего токенов {total_tokens} ")
#     # print(total_answer[0])
#     return total_answer


# async def run_main():
#     result = await main("Ваш вопрос")  # Замените "Ваш вопрос" на реальный вопрос
#     print(result[0])


# asyncio.run(run_main())

# def open_ai(quest):
#     stream = client.chat.completions.create(
#         model="gpt-3.5-turbo",#"gpt-4",
#         messages=[{"role": "user", "content": quest}],
#         stream=True,
#     )
#     # print(quest)
#     # for gh in stream:
#     #     print(gh)
#     for chunk in stream:
#          print(chunk.choices[0].delta.content or "", end="")
    

    # Предположим, что у нас есть объект stream, представляющий собой поток данных
    # В этом потоке есть набор объектов chunk, которые, вероятно, являются частью какой-то структуры данных

    # Итерируемся по всем chunk в потоке stream
    # for chunk in stream:
        
    #     # Получаем первый элемент (choices[0]) из списка choices в объекте chunk
    #     first_choice = chunk.choices[0]
        
    #     # Проверяем, существует ли свойство delta у объекта first_choice
    #     if hasattr(first_choice, 'delta'):
    #         # Если свойство delta существует, получаем объект delta и извлекаем свойство content
    #         delta_content = first_choice.delta.content
            
    #         # Печатаем значение свойства content, если оно не является пустой строкой
    #         if delta_content:
    #             print(delta_content, end="")
    #     else:
    #         # Если свойство delta отсутствует, выводим пустую строку
    #         print("", end="")

#open_ai(quest)






# from openai import AsyncOpenAI
# import asyncio

# client = AsyncOpenAI(
#     api_key=api_key,
# )

# async def main():
#     stream = await client.chat.completions.create(
#         model="gpt-3.5-turbo",#"gpt-4",
#         messages=[{"role": "user", "content": "Say this is a test"}],
#         stream=True,
#     )
#     async for chunk in stream:
#         print(chunk.choices[0].delta.content or "", end="")
# asyncio.run(main())




# def ffg
# # Предположим, у вас есть асинхронная функция, возвращающая поток данных
# async def main(text):
#     stream = await client.chat.completions.create(
#         model="gpt-3.5-turbo",#"gpt-4",
#         messages=[{"role": "user", "content": text}],
#         stream=True,
#     )
#     # Итерация по потоку данных
#     async for chunk in stream:
#         content = chunk.choices[0].delta.content or "" # Получение контента из текущего чанка
#         print(content, end="") # Печать контента без новой строки в конце


# asyncio.run(main(question))




# def open_ai(message):
#     # bot.send_message(message.chat.id, "hi")
#     #logger.info(f" - message_text:'{message.text}' - user_name:{message.from_user.username} - user_id:{message.from_user.id}")
#     # bot.reply_to(message, "hi")
#     # Собираем запрос Json к API Openai
#     question = message.text + " "# +patch
#     # print(question)

#     url = 'https://api.openai.com/v1/chat/completions'
#     headers = {
#         'Authorization': f'Bearer {api_key}',
#         'Content-Type': 'application/json'
#     }
#     data = {
#         "model": "gpt-3.5-turbo", # model,
#         "messages": [{"role": "user", "content": question}],
#         "temperature": 0.7, # temp,
#     }
#     response = requests.post(url, headers=headers, data=json.dumps(data))

#     response_data = response.json()  # Разбираем JSON-ответ

#     first_choice_message = response_data['choices'][0]['message']['content']
#     # print("\n", first_choice_message, "\n", temp)
#     return first_choice_message








# url = 'https://api.openai.com/v1/chat/completions'
# headers = {
#     'Authorization': f'Bearer {api_key}',
#     'Content-Type': 'application/json'
# }

# # Options ChatGPT
# patch = "Ответ не больше одного предложения." # Пока проверяю, экономлю)Ответ не больше трех предложений.
# temp = 0.7 # Уровень творчества от 0 до 1
# # temperature = 0, консервативные, наиболее вероятное следующее слово, ответы более детерминированные и менее разнообразные.
# # temperature = 1, увеличивает случайность в выборе слов, более разнообразные и творческие ответы, неожиданные результаты, вероятность нерелевантного или некорректного контента.
# model = "gpt-3.5-turbo"
# # gpt-4-1106-preview   150,000 TPM    500 RPM  (turbo)
# # gpt-3.5-turbo        60,000 TPM     500 RPM  (cheap)
# # gpt-4 
    



    # # Собираем запрос Json к API Openai
    # question = message.text + " " +patch
    # # print(question)
    # headers = {
    #     'Authorization': f'Bearer {api_key}',
    #     'Content-Type': 'application/json'
    # }
    # data = {
    #     "model": model,
    #     "messages": [{"role": "user", "content": question}],
    #     "temperature": temp,
    # }
    # response = requests.post(url, headers=headers, data=json.dumps(data))

    # response_data = response.json()  # Разбираем JSON-ответ

    # first_choice_message = response_data['choices'][0]['message']['content']
    # # print("\n", first_choice_message, "\n", temp)
    # bot.reply_to(message, first_choice_message)