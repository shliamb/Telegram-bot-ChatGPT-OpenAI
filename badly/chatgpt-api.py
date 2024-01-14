# Одноразовые вопросы к ChatGPT без связи
import requests
import json
import os

# Options chat
temp = 0.7
# temperature = 0, консервативные, наиболее вероятное следующее слово, ответы более детерминированные и менее разнообразные.
# temperature = 1, увеличивает случайность в выборе слов, более разнообразные и творческие ответы, неожиданные результаты, вероятность нерелевантного или некорректного контента.
question = "Что делает женщину счастливой в три слова"
model = "gpt-3.5-turbo" # or gpt-3.5-turbo
# gpt-4-1106-preview   150,000 TPM    500 RPM  (turbo)
# gpt-3.5-turbo        60,000 TPM     500 RPM  (cheap)
# gpt-4                10,000 TPM     500 RPM  (expensive)

api_key = os.environ.get('CHATGPT_API_KEY') # Переменная окружения
url = 'https://api.openai.com/v1/chat/completions'

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

data = {
     "model": model,
     "messages": [{"role": "user", "content": question}],
     "temperature": temp,
   }

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:  # Проверяем успешность запроса
    response_data = response.json()  # Разбираем JSON-ответ

    if 'choices' in response_data and len(response_data['choices']) > 0:
        first_choice_message = response_data['choices'][0]['message']['content']
        print("\n", first_choice_message, "\n")
    else:
        print("Ответ не содержит ожидаемых данных.")
else:
    print("Запрос завершился с кодом состояния:", response.status_code)


# allresp = response.json()
# print("\n", allresp)
# for key, value in allresp.items():
#     print(f"{key}: {value}")