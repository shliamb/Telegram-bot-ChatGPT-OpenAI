--
-- PostgreSQL database dump
--

-- Dumped from database version 15.5 (Debian 15.5-1.pgdg120+1)
-- Dumped by pg_dump version 15.5 (Ubuntu 15.5-0ubuntu0.23.10.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: discussion; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.discussion (
    id bigint NOT NULL,
    discus character varying(7000),
    "timestamp" timestamp without time zone NOT NULL
);


ALTER TABLE public.discussion OWNER TO admin;

--
-- Name: exchange; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.exchange (
    id integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    rate double precision DEFAULT '100'::double precision NOT NULL
);


ALTER TABLE public.exchange OWNER TO admin;

--
-- Name: exchange_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.exchange_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exchange_id_seq OWNER TO admin;

--
-- Name: exchange_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.exchange_id_seq OWNED BY public.exchange.id;


--
-- Name: settings; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.settings (
    id bigint NOT NULL,
    temp_chat double precision DEFAULT '0.7'::double precision NOT NULL,
    frequency double precision DEFAULT '0.5'::double precision NOT NULL,
    presence double precision DEFAULT '0.5'::double precision NOT NULL,
    flag_stik boolean DEFAULT false NOT NULL,
    all_count integer DEFAULT 0 NOT NULL,
    all_token integer DEFAULT 0 NOT NULL,
    the_gap double precision DEFAULT '0.05'::double precision NOT NULL,
    set_model character varying(50) DEFAULT 'gpt-3.5-turbo-0613'::character varying NOT NULL,
    give_me_money double precision DEFAULT '0'::double precision NOT NULL,
    money double precision DEFAULT '100'::double precision NOT NULL,
    all_in_money double precision DEFAULT '0'::double precision NOT NULL
);


ALTER TABLE public.settings OWNER TO admin;

--
-- Name: statistics; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.statistics (
    id integer NOT NULL,
    "time" timestamp without time zone NOT NULL,
    use_model character varying(50) NOT NULL,
    sesion_token integer DEFAULT 0 NOT NULL,
    price_1_tok double precision DEFAULT '0'::double precision NOT NULL,
    price_sesion_tok double precision DEFAULT '0'::double precision NOT NULL,
    users_telegram_id bigint
);


ALTER TABLE public.statistics OWNER TO admin;

--
-- Name: statistics_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.statistics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.statistics_id_seq OWNER TO admin;

--
-- Name: statistics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.statistics_id_seq OWNED BY public.statistics.id;


--
-- Name: users_db; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users_db (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(100) NOT NULL,
    email character varying(100)
);


ALTER TABLE public.users_db OWNER TO admin;

--
-- Name: users_db_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.users_db_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_db_id_seq OWNER TO admin;

--
-- Name: users_db_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.users_db_id_seq OWNED BY public.users_db.id;


--
-- Name: users_telegram; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.users_telegram (
    id bigint NOT NULL,
    name character varying(50),
    full_name character varying(50),
    first_name character varying(50),
    last_name character varying(50),
    chat_id bigint,
    is_admin boolean DEFAULT false NOT NULL,
    is_block boolean DEFAULT false NOT NULL,
    is_good integer DEFAULT 3 NOT NULL
);


ALTER TABLE public.users_telegram OWNER TO admin;

--
-- Name: users_telegram_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.users_telegram_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_telegram_id_seq OWNER TO admin;

--
-- Name: users_telegram_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.users_telegram_id_seq OWNED BY public.users_telegram.id;


--
-- Name: exchange id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.exchange ALTER COLUMN id SET DEFAULT nextval('public.exchange_id_seq'::regclass);


--
-- Name: statistics id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.statistics ALTER COLUMN id SET DEFAULT nextval('public.statistics_id_seq'::regclass);


--
-- Name: users_db id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_db ALTER COLUMN id SET DEFAULT nextval('public.users_db_id_seq'::regclass);


--
-- Name: users_telegram id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_telegram ALTER COLUMN id SET DEFAULT nextval('public.users_telegram_id_seq'::regclass);


--
-- Data for Name: discussion; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.discussion (id, discus, "timestamp") FROM stdin;
326950749	Что такое хрен\n Хрен - это овощное растение, близкое к роду луковых. Он имеет тонкий острый вкус и используется как приправа в пищевой промышленности, а также в кулинарии для добавления пикантности и остроты в различные блюда. Хрен может быть использован свежим, соленым или маринованным. Его также можно найти в виде готовых соусов или пасты.\n А хер?\n "Хер" - это русское нецензурное слово, которое используется для обозначения мужского полового члена. Оно является неприличным и нецензурным выражением, и его использование считается неприемлемым в формальных или уважительных ситуациях.\n Врешь\n Я - искусственный интеллект и не обладаю возможностью лгать или сознательно давать неправильную информацию. Моя цель - предоставлять точные и достоверные ответы на вопросы пользователей.\n Бестолковая железка\n "Бестолковая железка" - это выражение, которое может использоваться для описания устройства или предмета, который по мнению говорящего не выполняет свою функцию или не принесет никакой пользы. Это язвительное выражение, которое может быть использовано для критики или негативного описания предмета.\n Скорость света\n Скорость света в вакууме является одной из фундаментальных констант физики и составляет приблизительно 299 792 458 метров в секунду (м/с) или около 1 079 252 848,8 километров в час (км/ч). Это предельная скорость, с которой все информация и энергия могут перемещаться в пространстве. Скорость света играет важную роль в теории относительности Альберта Эйнштейна и занимает центральное место в современной физике.\n Скрипт на повершел бекап\n PowerShell — это мощный инструмент автоматизации и управления, который можно использовать для написания скриптов, в том числе и для резервного копирования (бекапа) данных. Ниже приведен пример скрипта на PowerShell для создания резервной копии папки:\n\n```powershell\n# Укажите путь к папке, которую нужно скопировать.\n$sourceFolder = "C:\\path\\to\\your\\source\\folder"\n\n# Укажите путь к папке назначения, где будут храниться бекапы.\n$destinationFolder = "D:\\path\\to\\your\\destination\\folder"\n\n# Создайте имя файла бекапа с помощью текущей даты и времени.\n$date = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"\n$backupFileName = "Backup_$date.zip"\n\n# Полный путь к файлу бекапа.\n$destinationPath = Join-Path $destinationFolder $backupFileName\n\n# Создание ZIP-архива с содержимым указанной папки.\nCompress-Archive -Path $sourceFolder -DestinationPath $destinationPath\n\nWrite-Host "Бекап '$sourceFolder' был успешно создан в '$destinationPath'"\n```\n\nЧтобы использовать этот скрипт:\n\n1. Замените `$sourceFolder` на путь к папке, которую вы хотите скопировать.\n2. Замените `$destinationFolder` на путь, где должны храниться бекапы.\n3. Сохраните код в файл с расширением `.ps1`, например `backup-script.ps1`.\n4. Запустите этот скрипт в PowerShell.\n\nОбратите внимание, что для запуска скриптов PowerShell может потребоваться изменение политики выполнения скриптов на вашем компьютере (с помощью команды `Set-ExecutionPolicy`). Используйте это с осторожностью и только если вы знаете, что делаете.\n\nТакже стоит отметить, что функция `Compress-Archive` требует PowerShell версии 5.0 или новее.\n\nДля сложных задач резервного копирования могут потребоваться дополнительные параметры и обработка ошибок; данный пример является базовым шаблоном для создания архивных копий папок.\n Настроить доверительные отношения между доменами\n Настройка доверительных отношений между доменами в среде Microsoft Active Directory (AD) позволяет пользователям одного домена авторизовываться в ресурсах другого домена. Это может быть необходимо, когда организации имеют несколько доменов AD и хотят облегчить доступ к ресурсам и управление ими.\n\nВот основные шаги для настройки доверительных отношений между двумя доменами:\n\n1. **Подготовка:**\n   - Убедитесь, что между контроллерами доменов есть сетевое соединение.\n   - Проверьте, что имя каждого домена уникально в пределах сети.\n   - Настройте DNS, чтобы обеспечить разрешение имен между всеми задействованными доменами.\n\n2. **Создание условий для trust:**\n   - Откройте "Active Directory Domains and Trusts" на контроллере домена.\n   - В левой панели щелкните правой кнопкой мыши по вашему домену и выберите "Properties".\n   - Перейдите на вкладку "Trusts" и нажмите "New Trust", затем следуйте инструкциям мастера создания новых доверительных отношений.\n\n3. **Выбор типа trust:**\n   - Выберите подходящий тип trust (например, односторонний или двусторонний).\n   \n4. **Настройка сторон trust:** \n   - Укажите имя другого домена и продолжайте следовать инструкциям мастера.\n   \n5. **Установление trust:**\n    - Выберите уровень аутентификации для trust (селективный или лесной).\n\n6. **Проверка trust:**\n    - Завершив настройку, используйте опцию "Verify" в мастере для проверки работоспособности созданных отношений.\n\n7. **Дополнительная конфигурация:**\n    - Может потребоваться настроить правила транзитивности или добавить SID-истории при переносе объектов между доменами.\n\n8. **Тестирование:**\n    - После создания dверительных отношений протестируйте их, попытавшись получить доступ к ресурсам из другого домена с использованием учетной записи из вашего первичного домена.\n\nЭти шаги являются обобщёнными; конкретные требования и процедуры могут изменяться в зависимости от версии Windows Server и конфигурации вашей инфраструктуры AD. Всегда следует тщательно спланировать любые изменения в AD и провести тестирование в контролируемой среде перед применением на продакшне.\n\nКроме того, при работе с dверительными отношениями стоит помнить о безопасности — неправильная конфигурация может повысить риск компрометации системы или данных.\n	2024-02-10 15:55:06.51267
1666495	python. \naiogram.\nпапка /data/\nВ папке проверить файлы, оставить последние 3 созданные, а остальные удалить, последний скачать.\n Чтобы реализовать описанную задачу на языке Python с использованием библиотеки aiogram, вам нужно будет выполнить несколько шагов:\n\n1. Получить список файлов в директории `/data/`.\n2. Отсортировать файлы по дате создания.\n3. Удалить все кроме последних трёх созданных файлов.\n4. Скачать последний (новейший) из оставшихся.\n\nВот пример скрипта, который выполняет эти шаги без использования aiogram, так как aiogram - это фреймворк для создания ботов в Telegram и не относится напрямую к управлению файлами на локальной машине:\n\n```python\nimport os\nfrom pathlib import Path\n\n# Путь к папке с данными\ndata_folder = Path("/data/")\n\n# Получаем список всех файлов в директории\nfiles = [entry for entry in data_folder.iterdir() if entry.is_file()]\n\n# Сортируем список файлов по дате изменения (от новых к старым)\nsorted_files = sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)\n\n# Оставляем последние 3 файла, удаляем остальные\nfor file_to_delete in sorted_files[3:]:\n    os.remove(file_to_delete)\n\n# Последний скачанный файл будет первым в отсортированном списке (новейшим)\nlast_downloaded_file = sorted_files[0] if sorted_files else None\n\n# Здесь можно добавить код для скачивания файла last_downloaded_file,\n# если имелось в виду "скачать" через интернет или переместить его.\n```\n\nЕсли вы хотите интегрировать эту функциональность в бота на базе aiogram и предполагается, что скачивание происходит через Telegram (например, отправка файла пользователю), то потребуется другой подход с использованием асинхронных функций aiogram для отправки файла.\n\nВажно: перед запуском кода убедитесь, что путь `/data/` корректен и доступен для записи и чтения вашей программой. В данном примере используется модуль `pathlib`, который является частью стандартной библиотеки Python и предоставляет объектно-ориентированный интерфейс для работы с файловой системой.\n	2024-02-11 01:57:04.123749
176513890	Требуется программа на python которая будет подберать коробку под детали. В коробку требуется поместить 500 деталей. Требуется из имеющихся найти \nоптимальную коробку. Так же нужно учесть что должен быть небольшой отступ от одной стенки по ширине и одной по длине от 3 до 10 мм. На ребро детали укладывать нельзя. \nЕсть список коробок [899*58*100,699*350*86,250*250*89,136*350*78, 106*250*110], габариты коробки записаны = длина*ширина*высота.\nЕсть габариты детали = 40*20*4.5, формат такой же = длина*ширина*высота.\n\n\nСоответсвенно у нас два варианта, как укладывать детали в коробку по ширине или по длине. Программа должна высчитытать в каком положении будет максимальное количество.\nПример. Деталь у меня не делится, значит деление происходит без остатка. \nКоробка у меня 405*105*200 и деталь у меня 40*10*5. Соответсвеноо в начале я делю 405/40 = 10  и   405/10 =40 \nЗатем я делю 105/40 = 2 и 105/10 = 10\nВ итоге у меня получается \n10 и 10 соответсвенно 100\n40 и 2 соответсвенно 80\n100>80 Значит укладываем по длине детали.\n\nВ итоге программа должна будет создать словарь где ключ будет габариты коробки, а значением количество вмещаемых деталей. Затем программа проходит по value ищет число \nкоторое больше всего приближено к 500.\n Вот пример программы на Python, которая решает вашу задачу:\n\n```python\nboxes = [\n    "899*58*100",\n    "699*350*86",\n    "250*250*89",\n    "136*350*78",\n    "106*250*110"\n]\n\npart_size = "40*20*4.5"\n\npart_length, part_width, part_height = map(float, part_size.split("*"))\n\nmax_count = 0\nbest_box = ""\n\nfor box in boxes:\n    box_length, box_width, box_height = map(float, box.split("*"))\n\n    # Check if the part can fit along the length of the box\n    length_fit = int(box_length // part_length)\n    width_fit = int(box_width // part_width)\n\n    count_by_length = length_fit * width_fit\n\n    # Check if the part can fit along the width of the box\n    length_fit = int(box_length // part_width)\n    width_fit = int(box_width // part_length)\n\n    count_by_width = length_fit * width_fit\n\n    count = max(count_by_length, count_by_width)\n\n    if count > max_count:\n        max_count = count\n        best_box = box\n\nresult_dict = {best_box: max_count}\n\nprint(result_dict)\n```\n\nЭта программа перебирает все коробки из списка `boxes` и вычисляет количество деталей, которое может поместиться в каждую коробку. Затем она сохраняет результат в словарь `result_dict`, где ключ - это размеры оптимальной коробки, а значение - количество вмещаемых деталей.\n\nПосле выполнения программы будет выведен словарь с оптимальной коробкой и количеством вмещаемых деталей.\n Требуется программа на python которая будет подберать коробку под детали. В коробку требуется поместить 500 деталей. Требуется из имеющихся найти \nоптимальную коробку. Так же нужно учесть что должен быть небольшой отступ от одной стенки по ширине и одной по длине от 3 до 10 мм. На ребро детали укладывать нельзя. \nЕсть список коробок [899*58*100,699*350*86,250*250*89,136*350*78, 106*250*110], габариты коробки записаны = длина*ширина*высота.\nЕсть габариты детали = 40*20*4.5, формат такой же = длина*ширина*высота.\n\n\nСоответсвенно у нас два варианта, как укладывать детали в коробку по ширине или по длине. Программа должна высчитытать в каком положении будет максимальное количество.\nПример. Деталь у меня не делится, значит деление происходит без остатка. \nКоробка у меня 405*105*200 и деталь у меня 40*10*5. Соответсвеноо в начале я делю 405/40 = 10  и   405/10 =40 \nЗатем я делю 105/40 = 2 и 105/10 = 10\nВ итоге у меня получается \n10 и 10 соответсвенно 100\n40 и 2 соответсвенно 80\n100>80 Значит укладываем по длине детали.\n\nВ итоге программа должна будет создать словарь где ключ будет габариты коробки, а значением количество вмещаемых деталей. Затем программа проходит по value ищет число \nкоторое больше всего приближено к 500.\n Программа, представленная ниже, учитывает требования к отступам и стремится подобрать коробку, в которую можно поместить как можно больше деталей, но не менее 500. Она создаёт словарь с коробками и количеством деталей, которые могут быть вмещены в каждую из них. Затем программа находит оптимальную коробку, вместимость которой наиболее близка к 500 деталям или превышает это число.\n\n```python\nboxes = [\n    "899*58*100",\n    "699*350*86",\n    "250*250*89",\n    "136*350*78",\n    "106*250*110"\n]\n\npart_size = "40*20*4.5"\n\n# Размеры детали\npart_length, part_width, part_height = map(float, part_size.split("*"))\n\n# Словарь для хранения результатов\nbox_capacity_dict = {}\n\nfor box in boxes:\n    # Размеры коробки\n    box_length, box_width, box_height = map(float, box.split("*"))\n    \n    # Учёт отступа от стенок (минимальный отступ 3 мм)\n    effective_box_length = box_length - 3\n    effective_box_width = box_width - 3\n\n    # Проверка по длине и ширине без переворота детали\n    length_fit_a = int(effective_box_length // part_length)\n    width_fit_a = int(effective_box_width // part_width)\n\n    count_a = length_fit_a * width_fit_a\n\n    # Проверка с переворотом детали (по ширине)\n    length_fit_b = int(effective_box_length // part_width)\n    width_fit_b = int(effective_box_width // part_length)\n\n    count_b = length_fit_b * width_fit_b\n\n    # Высота позволяет уложить слоёв\n    layers_count = int(box_height // part_height)\n\n    max_count_in_box = max(count_a, count_b) * layers_count\n\n    # Заполнение словаря возможными вариантами упаковки с количеством деталей\n    if max_count_in_box > 0: \n        box_capacity_dict[box] = max_count_in_box\n\n# Ищем оптимальную коробку с количеством ближайшим к 500 или больше\nclosest_to_500_capacity_key_val_pair = None\n\nfor key in sorted(box_capacity_dict.keys(), key=lambda x: (abs(500-box_capacity_dict[x]), -box_capacity_dict[x])):\n   if closest_to_500_capacity_key_val_pair is None or abs(500-box_capacity_dict[key]) < abs(500-closest_to_500_capacity_key_val_pair[1]):\n       closest_to_500_capacity_key_val_pair = (key, box_capacity_dict[key])\n       if closest_to_500_capacity_key_val_pair[1] >= 500:\n           break\n\nprint(f"Оптимальная коробка: {closest_to_500_capacity_key_val_pair}")\n\n```\n\nЭта программа учитывает минимальный отступ от стенок при расчётах возможности размещения деталей и выбирает ту коробку из списка, которая может содержать количество деталей наиболее близкое к 500 или больше.\n\n	2024-02-10 15:24:07.199158
\.


--
-- Data for Name: exchange; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.exchange (id, "timestamp", rate) FROM stdin;
1	2024-02-11 01:57:02.408472	90.89
\.


--
-- Data for Name: settings; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.settings (id, temp_chat, frequency, presence, flag_stik, all_count, all_token, the_gap, set_model, give_me_money, money, all_in_money) FROM stdin;
176513890	0.7	0.5	0.5	f	2	3262	0.05	gpt-4-0125-preview	0	82.69781604	0
326950749	0.7	0.5	0.5	f	7	5329	0.05	gpt-4-1106-preview	0	69.38333993999998	0
1666495	0.7	0.5	0.5	t	11	905	0.05	gpt-4-1106-preview	0	994.8588980400002	0
\.


--
-- Data for Name: statistics; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.statistics (id, "time", use_model, sesion_token, price_1_tok, price_sesion_tok, users_telegram_id) FROM stdin;
1	2024-02-10 11:58:14.741984	gpt-3.5-turbo-0613	18	0.0005453400000000001	0.009816120000000001	1666495
2	2024-02-10 12:01:28.763595	gpt-3.5-turbo-0613	18	0.0005453400000000001	0.009816120000000001	1666495
3	2024-02-10 12:02:43.749953	gpt-3.5-turbo-0613	29	0.0005453400000000001	0.01581486	1666495
4	2024-02-10 12:02:53.507318	gpt-3.5-turbo-0613	40	0.0005453400000000001	0.021813600000000002	1666495
5	2024-02-10 12:12:59.050896	gpt-3.5-turbo-0613	18	0.0005453400000000001	0.009816120000000001	1666495
6	2024-02-10 12:57:29.435921	gpt-3.5-turbo-0613	18	0.0005453400000000001	0.009816120000000001	1666495
7	2024-02-10 13:21:19.789173	gpt-3.5-turbo-0613	18	0.0005453400000000001	0.009816120000000001	1666495
8	2024-02-10 13:30:23.546507	gpt-3.5-turbo-0613	19	0.0005453400000000001	0.010361460000000001	1666495
9	2024-02-10 13:38:01.780676	gpt-3.5-turbo-0613	18	0.0005453400000000001	0.009816120000000001	1666495
10	2024-02-10 13:56:04.630956	gpt-3.5-turbo-0613	18	0.0005453400000000001	0.009816120000000001	1666495
11	2024-02-10 15:21:16.062785	gpt-3.5-turbo-0613	954	0.0005453400000000001	0.52025436	176513890
12	2024-02-10 15:24:06.839287	gpt-4-0125-preview	2308	0.0072712	16.7819296	176513890
13	2024-02-10 15:46:12.424821	gpt-3.5-turbo-0613	157	0.0005453400000000001	0.08561838000000001	326950749
14	2024-02-10 15:46:22.120168	gpt-3.5-turbo-0613	258	0.0005453400000000001	0.14069772000000003	326950749
15	2024-02-10 15:47:06.695761	gpt-3.5-turbo-0613	336	0.0005453400000000001	0.18323424000000002	326950749
16	2024-02-10 15:47:37.928825	gpt-3.5-turbo-0613	458	0.0005453400000000001	0.24976572000000002	326950749
17	2024-02-10 15:49:15.974378	gpt-4-1106-preview	654	0.0072712	4.7553648	326950749
18	2024-02-10 15:50:14.445288	gpt-4-1106-preview	1287	0.0072712	9.358034400000001	326950749
19	2024-02-10 15:55:06.131076	gpt-4-1106-preview	2179	0.0072712	15.843944800000001	326950749
20	2024-02-11 01:57:03.792548	gpt-4-1106-preview	691	0.0072712	5.0243992	1666495
\.


--
-- Data for Name: users_db; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users_db (id, username, password, email) FROM stdin;
\.


--
-- Data for Name: users_telegram; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.users_telegram (id, name, full_name, first_name, last_name, chat_id, is_admin, is_block, is_good) FROM stdin;
1666495	Shliambur	Shliamb	Shliamb	\N	1666495	t	f	3
176513890	\N	Andrey Xu	Andrey	Xu	176513890	f	f	3
326950749	\N	Serg	Serg	\N	326950749	f	f	3
\.


--
-- Name: exchange_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.exchange_id_seq', 1, false);


--
-- Name: statistics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.statistics_id_seq', 20, true);


--
-- Name: users_db_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.users_db_id_seq', 1, false);


--
-- Name: users_telegram_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.users_telegram_id_seq', 1, false);


--
-- Name: discussion discussion_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.discussion
    ADD CONSTRAINT discussion_pkey PRIMARY KEY (id);


--
-- Name: exchange exchange_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.exchange
    ADD CONSTRAINT exchange_pkey PRIMARY KEY (id);


--
-- Name: settings settings_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.settings
    ADD CONSTRAINT settings_pkey PRIMARY KEY (id);


--
-- Name: statistics statistics_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.statistics
    ADD CONSTRAINT statistics_pkey PRIMARY KEY (id);


--
-- Name: users_db users_db_email_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_db
    ADD CONSTRAINT users_db_email_key UNIQUE (email);


--
-- Name: users_db users_db_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_db
    ADD CONSTRAINT users_db_pkey PRIMARY KEY (id);


--
-- Name: users_db users_db_username_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_db
    ADD CONSTRAINT users_db_username_key UNIQUE (username);


--
-- Name: users_telegram users_telegram_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.users_telegram
    ADD CONSTRAINT users_telegram_pkey PRIMARY KEY (id);


--
-- Name: ix_statistics_users_telegram_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_statistics_users_telegram_id ON public.statistics USING btree (users_telegram_id);


--
-- Name: ix_users_db_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_users_db_id ON public.users_db USING btree (id);


--
-- Name: ix_users_telegram_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE UNIQUE INDEX ix_users_telegram_id ON public.users_telegram USING btree (id);


--
-- Name: discussion discussion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.discussion
    ADD CONSTRAINT discussion_id_fkey FOREIGN KEY (id) REFERENCES public.users_telegram(id);


--
-- Name: settings settings_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.settings
    ADD CONSTRAINT settings_id_fkey FOREIGN KEY (id) REFERENCES public.users_telegram(id);


--
-- Name: statistics statistics_users_telegram_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.statistics
    ADD CONSTRAINT statistics_users_telegram_id_fkey FOREIGN KEY (users_telegram_id) REFERENCES public.users_telegram(id);


--
-- PostgreSQL database dump complete
--

