from keys import api_key

def test_openai():
    print(api_key[:5])



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