
# RU

## Что это?
Это простой телеграм бот. Он дает прямой доступ к ChatGPT 3.5, ChatGPT 4 Turbo, ChatGPT 4 и др.

## Для кого это?
Для тех людей, кто вынужден находиться в стране, находящейся под санкциями, а VPN постоянно блокируется и постоянно виснет. Для тех, кто не может себе позволить 20$ в месяц на последнюю версию ChatGPT от OpenAI.
Этот бот позволяет пользоваться оригинальным ChatGPT экономно, дозированно. Оплата только за токены. К примеру, я пользуюсь на постоянной основе GPT-3.5, но когда он не справляется, переключаюсь на GPT-4, выходит очень дешево.

Этот бот не нужен тем, кто не в санкциях, вы можете просто скачать официально пользоваться приложением от OpenAI. 3.5 бесплатный, 4 - придется оплатить.

## Как пользоваться?
1. Выбрать сервер без санкций, установить приложение, зарегиться в OpenAI, закинуть 5$ и пользоваться.
2. Можете просто пользоваться моим - https://t.me/shliamb2_bot Можно просто попробовать.


<img src="https://raw.githubusercontent.com/shliamb/Telegram-bot-ChatGPT-OpenAI/main/img/bot.png" alt="ChatGPT" width="auto" height="auto" align="top">

<img src="https://raw.githubusercontent.com/shliamb/Telegram-bot-ChatGPT-OpenAI/main/img/bot4.png" alt="ChatGPT" width="auto" height="auto" align="top">

<img src="https://raw.githubusercontent.com/shliamb/Telegram-bot-ChatGPT-OpenAI/main/img/bot5.png" alt="ChatGPT" width="auto" height="auto" align="top">


Основные технологии и библиотеки:
1. Aiogram 3.3.0,
2. Anyio 4.2.0
3. Alembic 1.13.1
4. Openai 1.11.1
5. SQLAlchemy 2.0.25
6. WalletPay 1.3.1
7. YooMoney 0.1.0
и др.


## Как работает
- База на PostgreSQL, работает асинхронно, в контейнере докера. Работа с базой через SQLAlchemy. В базе хранятся основные данные и настройки пользователя, счет. Статистика трат, которые клиент может скачать через настройки бота. Так же в базе храниться курс RUB - USD. Он обновляется раз в день через сервер центробанка. Так же в ячейке базы на каждого пользователя сохраняется на выбранный период переписка с ChatGPT для того что бы чат, имел контекст общения. Даную функцию можно удалить или выставить нужное время в настройках бота.

- На данный момент можно пополнить баланс спомощью оплаты картой через Yoomoney, оплатой через WALLET PAY, переводом крипты.

- Раз в сутки база данных сохраняется в папку на сервере. 

- Есть админ меню, доступное администратору. В нем можно скачать файл базы данных, там же в онлайне можно остановить сессии, очистить базу и залить свою. Там же можно посмотреть всю статистику. Скачать файл логов, там же можно его очистить.

- Запуск на сервере сводиться к клонированию репозитория, к правке в ручную файла .env, в него нужно вписать все ключи и токены. Токен OpenAI нужно вносить на сервере руками, так как при обнаружении его на GitHab, его действие на OpenAI прекращается.




# EN

## What is it?
This is a simple telegram bot. It gives direct access to ChatGPT 3.5, ChatGPT 4 Turbo, ChatGPT 4, etc.

## Who is this for?
For those people who are forced to stay in a country under sanctions, and the VPN is constantly blocked and constantly hanging. For those who can't afford $20 per month for the latest version of ChatGPT from OpenAI.
This bot allows you to use the original ChatGPT sparingly, in a dosed manner. Payment is only for tokens. For example, I use GPT-3.5 on a regular basis, but when it fails, I switch to GPT-4, it comes out very cheap.

This bot is not needed by those who are not in sanctions, you can just download and officially use the application from OpenAI. 3.5 is free, 4 - you will have to pay.

## How to use it?
1. Select a server without sanctions, install the application, sign up for OpenAI, throw in $ 5 and use it.
2. You can just use my - https://t.me/shliamb2_bot You can just try it.

<img src="https://raw.githubusercontent.com/shliamb/Telegram-bot-ChatGPT-OpenAI/main/img/bot.png" alt="ChatGPT" width="auto" height="auto" align="top">

<img src="https://raw.githubusercontent.com/shliamb/Telegram-bot-ChatGPT-OpenAI/main/img/bot4.png" alt="ChatGPT" width="auto" height="auto" align="top">

<img src="https://raw.githubusercontent.com/shliamb/Telegram-bot-ChatGPT-OpenAI/main/img/bot5.png" alt="ChatGPT" width="auto" height="auto" align="top">


Main technologies and libraries:
1. Aiogram 3.3.0,
2. Anyio 4.2.0
3. Alembic 1.13.1
4. Openai 1.11.1
5. SQLAlchemy 2.0.25
6. WalletPay 1.3.1
7. YooMoney 0.1.0
, etc.


## How it works
- The database is based on PostgreSQL, it works asynchronously, in a docker container. Working with the database via SQLAlchemy. The database stores the basic data and user settings, the account. Statistics of expenses that the client can download through the bot settings. The RUB - USD exchange rate is also stored in the database. It is updated once a day via the central bank's server. Also, in the database cell for each user, correspondence with ChatGPT is stored for the selected period in order for the chat to have a communication context. You can delete this function or set the desired time in the bot settings.

- At the moment, you can top up your balance by paying with a card via Yoomoney, paying via WALLET PAY, or transferring crypts.

- Once a day, the database is saved to a folder on the server. 

- There is an admin menu available to the administrator. You can download a database file in it, you can also stop sessions online, clear the database and fill in your own. You can also view all the statistics there. Download the log file, you can also clear it there.

- Running on the server boils down to cloning the repository, manually editing the .env file, you need to enter all the keys and tokens into it. The OpenAI token must be entered on the server by hand, since when it is detected on GitHab, its effect on OpenAI stops.
