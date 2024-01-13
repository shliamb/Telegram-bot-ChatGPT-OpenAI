# Strem
#import requests
#import json
import os
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key = os.environ.get('CHATGPT_API_KEY') # Переменная окружения,
)
question = "Как тебя зовут, меня Саша"
model = "gpt-3.5-turbo" # or gpt-3.5-turbo
# gpt-4-1106-preview   150,000 TPM    500 RPM  (turbo)
# gpt-3.5-turbo        60,000 TPM     500 RPM  (cheap)
# gpt-4                10,000 TPM     500 RPM  (expensive)

async def main():
    stream = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": question}],
        stream=True,
    )
    async for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")


asyncio.run(main())