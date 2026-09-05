# Настройка Supabase для Female-Fabric

## Шаг 1: Создание проекта в Supabase

1. Зайдите на [supabase.com](https://supabase.com) и создайте бесплатный аккаунт
2. Создайте новый проект:
   - Название: `female-fabric` (или любое другое)
   - Database Password: **сохраните пароль!**
   - Region: выберите ближайший регион (Europe для России)

## Шаг 2: Инициализация базы данных

1. Откройте **SQL Editor** в Supabase Dashboard
2. Выполните SQL-скрипт из файла `supabase-schema.sql` (скопируйте и вставьте весь текст)
3. Нажмите **Run** для создания таблиц

Альтернативно, можно запустить скрипт локально:

```bash
python scripts/init_db.py
```

## Шаг 3: Получение Connection String

1. В Supabase Dashboard откройте: **Project Settings** → **Database**
2. Найдите **Connection String** → выберите режим **Session** (pooler)
3. Скопируйте строку подключения, она выглядит так:

```
postgresql://postgres.xxxxxxxxxxxxx:[YOUR-PASSWORD]@aws-0-eu-central-1.pooler.supabase.com:6543/postgres
```

4. **ВАЖНО:** Замените `postgresql://` на `postgresql+pg8000://` для совместимости с pg8000 драйвером
5. Замените `[YOUR-PASSWORD]` на ваш реальный пароль базы данных

## Шаг 4: Настройка для локальной разработки

Откройте `.env` файл и замените DATABASE_URL:

```bash
DATABASE_URL=postgresql+pg8000://postgres.xxxxxxxxxxxxx:YOUR_PASSWORD@aws-0-eu-central-1.pooler.supabase.com:6543/postgres
```

Запустите приложение локально для проверки:

```bash
python run.py
```

## Шаг 5: Настройка секретов для Cloudflare Workers

Для деплоя на Cloudflare Workers нужно установить секреты через Wrangler CLI:

```bash
# SECRET_KEY - секретный ключ для JWT токенов (сгенерируйте новый!)
npx wrangler secret put SECRET_KEY
# Введите: любая случайная строка минимум 32 символа

# DATABASE_URL - строка подключения к Supabase
npx wrangler secret put DATABASE_URL
# Введите вашу строку: postgresql+pg8000://postgres.xxx...

# Опционально: если используете Supabase Storage для загрузки картинок
npx wrangler secret put SUPABASE_URL
# Введите: https://YOUR_PROJECT_REF.supabase.co

npx wrangler secret put SUPABASE_KEY
# Введите ваш service_role key из Project Settings → API
```

## Шаг 6: Деплой на Cloudflare Workers

После настройки секретов выполните деплой:

```bash
# Через uv (рекомендуется)
uv run pywrangler deploy

# Или через стандартный wrangler
npx wrangler deploy
```

## Проверка работоспособности

После деплоя:
1. Откройте URL вашего Worker (например, `https://female-fabric.workers.dev`)
2. Попробуйте зарегистрироваться или войти с тестовыми данными:
   - Email: `admin@female-fabric.ru`
   - Пароль: `[SECURE_ADMIN_PASSWORD]`

## Troubleshooting

### Ошибка подключения к базе данных

- Проверьте правильность connection string
- Убедитесь что используете `postgresql+pg8000://` (не `postgres://`)
- Проверьте что пароль не содержит специальных символов, требующих URL-кодирования

### Таблицы не создаются автоматически

- Установите `AUTO_CREATE_TABLES=true` в переменных окружения
- Или запустите `supabase-schema.sql` вручную через SQL Editor

### Ошибки при деплое на Cloudflare

- Убедитесь что все секреты установлены через `wrangler secret put`
- Проверьте что `pg8000>=1.30.0` есть в `pyproject.toml`
- Убедитесь что нет зависимостей от bcrypt, pillow или других несовместимых пакетов
