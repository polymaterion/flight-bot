# Bilet Bot — Telegram-бот поиска авиабилетов в Туркменистан

Бот на aiogram 3 для поиска цен на авиабилеты между городами СНГ и Туркменистана,
с поддержкой подписок на маршруты и уведомлениями о появлении/снижении цены.

## Как это устроено (важно прочитать)

Travelpayouts даёт два разных API:

1. **Flight Search API (real-time поиск)** — тот самый "живой" поиск с точными
   ценами и мгновенным результатом. Доступен **только проектам с подтверждённым
   MAU от 50 000 пользователей**. Для нового бота недоступен в принципе — заявку
   без готового трафика там даже не рассматривают.
2. **Aviasales Data API** — открыт всем, без ограничений по трафику. Отдаёт
   цены из кэша, собранного по реальным поискам других пользователей Aviasales
   за последние 48 часов – 7 дней. Это не "live"-цена именно сейчас, а хорошая
   актуальная оценка + прямая ссылка на Aviasales, где при клике пользователь
   увидит уже реальные текущие варианты и купит билет по вашей партнёрской ссылке.

Этот бот построен на **Data API** — это единственный реалистичный вариант для
старта. Когда у бота наберётся 50 000+ MAU, эндпоинты в
`bot/services/travelpayouts.py` можно заменить на настоящий Flight Search API
(структура кода это позволяет без переписывания хендлеров).

## Структура проекта

```
bot/
  main.py                     — точка входа, сборка бота и планировщика
  config.py                   — чтение .env
  data/cities.py               — справочник городов + логика "откуда/куда"
  locales/texts.py             — все тексты на ru/tk
  db/database.py               — PostgreSQL (asyncpg), таблицы users/subscriptions
  services/travelpayouts.py    — клиент Aviasales Data API + партнёрские ссылки
  services/subscription_checker.py — фоновая проверка цен по подпискам
  handlers/start.py            — /start и выбор языка
  handlers/settings.py         — смена языка
  handlers/search.py           — весь флоу поиска билетов (FSM)
  handlers/subscriptions.py    — просмотр/удаление подписок
  keyboards/                   — inline и reply клавиатуры
```

## Установка

### 1. Клонировать/скопировать проект и создать окружение

```bash
cd tkm_bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Настроить PostgreSQL

Создайте базу и пользователя:

```sql
CREATE DATABASE tkm_bot;
CREATE USER tkm_bot WITH PASSWORD 'ваш_пароль';
GRANT ALL PRIVILEGES ON DATABASE tkm_bot TO tkm_bot;
```

Таблицы `users` и `subscriptions` бот создаёт сам при первом запуске
(см. `bot/db/database.py -> _create_tables`), вручную ничего создавать не нужно.

### 3. Заполнить .env

```bash
cp .env.example .env
```

Откройте `.env` и укажите:
- `BOT_TOKEN` — токен от @BotFather
- `TP_TOKEN` — ваш API-токен Travelpayouts (Личный кабинет → API)
- `TP_MARKER` — ваш partner marker (тот же кабинет, раздел "Инструменты" / рекламные ссылки)
- данные подключения к PostgreSQL

### 4. Запустить бота

```bash
python -m bot.main
```

Бот запустится в режиме polling. Для продакшена рекомендуется запускать
через systemd или supervisor, чтобы бот автоматически перезапускался при сбое.

Пример unit-файла systemd (`/etc/systemd/system/tkm-bot.service`):

```ini
[Unit]
Description=Turkmenistan Tickets Telegram Bot
After=network.target postgresql.service

[Service]
Type=simple
WorkingDirectory=/opt/tkm_bot
ExecStart=/opt/tkm_bot/venv/bin/python -m bot.main
Restart=always
RestartSec=5
EnvironmentFile=/opt/tkm_bot/.env

[Install]
WantedBy=multi-user.target
```

## Пользовательский флоу

1. `/start` → выбор языка (🇷🇺 Русский / 🇹🇲 Türkmençe)
2. Приветствие + reply-клавиатура: **Найти билеты / Мои подписки / Настройки**
3. **Найти билеты**:
   - Откуда (все города ТКМ + Москва/СПб/Казань/Минск/Екатеринбург/Самара/Новосибирск)
   - Куда (если "откуда" не ТКМ — только города ТКМ; если "откуда" ТКМ — все города,
     включая другие города ТКМ — так поддерживаются внутренние рейсы)
   - Дата (этот месяц / следующий месяц / указать дату / указать диапазон)
   - Превью маршрута → Подтвердить
   - Результаты (карточки с ценой и кнопкой "Купить билет" по партнёрской ссылке),
     либо предложение подписаться, если данных о цене пока нет
4. **Мои подписки** — список, у каждой кнопка удаления
5. **Настройки** — смена языка в любой момент

## Как расширить

- **Добавить города**: правки только в `bot/data/cities.py`, весь остальной код
  подхватит новые города автоматически (кнопки, направления, локализация).
- **Добавить язык**: добавить ключ в каждый словарь `bot/locales/texts.py`
  и завести третью кнопку в `language_choice_kb` / `settings_kb`.
- **Перейти на настоящий Flight Search API** после набора 50k MAU: переписать
  `TravelpayoutsClient.find_prices` на вызовы нового `/v1/flight_search`-подобного
  эндпоинта — интерфейс класса (метод `find_prices` возвращающий `PriceOption`)
  можно оставить прежним, чтобы не трогать хендлеры.
