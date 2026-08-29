# 🚀 Быстрый старт Female-Fabric

## Локальный запуск (разработка)

### Шаг 1: Установка зависимостей

```bash
pip install -r requirements.txt
```

### Шаг 2: Проверка конфигурации

Убедитесь что файл `.env` существует и содержит настройки для SQLite:

```bash
DATABASE_URL=sqlite:///./female_fabric.db
AUTO_CREATE_TABLES=true
```

### Шаг 3: Запуск сервера

```bash
python run.py
```

Сервер запустится на `http://localhost:8000`

### Шаг 4: Проверка работоспособности

Откройте в браузере:
- Главная страница: http://localhost:8000
- API документация: http://localhost:8000/docs
- Админ панель: http://localhost:8000/admin

**Тестовые учетные записи:**
- Админ: `admin@female-fabric.ru` / `Admin123!`
- Пользователь: `user@female-fabric.ru` / `User123!`

---

## Деплой на Cloudflare Workers

### Предварительные требования

1. Установите Node.js и npm
2. Установите Wrangler CLI:
   ```bash
   npm install -g wrangler
   ```

3. Установите uv (опционально, но рекомендуется):
   ```bash
   pip install uv
   ```

### Шаг 1: Настройте Supabase

Следуйте инструкциям в файле `SUPABASE_SETUP.md`

### Шаг 2: Установите секреты Cloudflare

```bash
# Авторизуйтесь в Cloudflare
wrangler login

# Установите секреты
wrangler secret put SECRET_KEY
# Введите случайную строку минимум 32 символа

wrangler secret put DATABASE_URL
# Введите строку подключения к Supabase:
# postgresql+pg8000://postgres.xxx:password@aws-0-eu-central-1.pooler.supabase.com:6543/postgres
```

### Шаг 3: Деплой

```bash
# Через uv (рекомендуется)
uv run pywrangler deploy

# Или через стандартный wrangler
wrangler deploy
```

### Шаг 4: Проверка

Откройте URL вашего Worker:
```
https://female-fabric.workers.dev
```

---

## Структура проекта

```
female-fabric/
├── app/                    # Основной код приложения
│   ├── api/               # API endpoints
│   ├── core/              # Безопасность, зависимости
│   ├── models/            # SQLAlchemy модели
│   ├── schemas/           # Pydantic схемы
│   ├── static/            # CSS, JS, изображения
│   ├── templates/         # HTML шаблоны
│   ├── config.py          # Настройки
│   ├── database.py        # Подключение к БД
│   └── main.py            # FastAPI приложение
├── public/                # Статика для Workers Static Assets
├── src/
│   └── worker.py          # Cloudflare Worker entrypoint
├── scripts/
│   └── init_db.py         # Инициализация БД
├── .env                   # Локальные переменные окружения
├── pyproject.toml         # Python зависимости для Workers
├── requirements.txt       # Зависимости для локальной разработки
├── wrangler.jsonc         # Конфигурация Cloudflare
├── run.py                 # Локальный запуск через uvicorn
└── test_app.py            # Автотесты
```

---

## Запуск тестов

```bash
python test_app.py
```

---

## Troubleshooting

### Ошибка импорта модулей

Переустановите зависимости:
```bash
pip install -r requirements.txt --force-reinstall
```

### База данных не инициализируется

Убедитесь что `AUTO_CREATE_TABLES=true` в `.env` файле, или запустите вручную:
```bash
python scripts/init_db.py
```

### Ошибки при деплое на Cloudflare

1. Проверьте что `pg8000` добавлен в зависимости
2. Убедитесь что нет bcrypt, pillow или других несовместимых пакетов
3. Проверьте логи через `wrangler tail`

### Проблемы с подключением к Supabase

1. Используйте Session pooler (порт 6543), а не прямое подключение
2. Замените `postgresql://` на `postgresql+pg8000://`
3. Убедитесь что пароль не содержит спецсимволов или экранируйте их

---

## Полезные команды

```bash
# Просмотр логов Worker в реальном времени
wrangler tail

# Локальная эмуляция Worker
wrangler dev

# Управление секретами
wrangler secret list
wrangler secret delete SECRET_NAME

# Просмотр информации о Worker
wrangler deployments list
```

---

## Что дальше?

1. ✅ Настройте Supabase Storage для загрузки изображений товаров
2. ✅ Добавьте свой домен в Cloudflare Workers
3. ✅ Настройте CI/CD через GitHub Actions (см. `.github/workflows/deploy.yml`)
4. ✅ Добавьте мониторинг и аналитику
5. ✅ Кастомизируйте дизайн под ваш бренд

**Удачи с запуском Female-Fabric! 🎉**
