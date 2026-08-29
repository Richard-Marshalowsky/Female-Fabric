# Female-Fabric — Интернет-магазин женской одежды

Современный, быстрый и адаптивный коммерческий интернет-магазин женской одежды премиум-класса **Female-Fabric**. 

Проект адаптирован для бессерверного запуска на **Cloudflare Python Workers** с использованием **FastAPI**, **SQLAlchemy ORM (PostgreSQL / Supabase / SQLite)**, **Pydantic v2**, безопасной аутентификации **JWT (bcrypt)** и **Workers Static Assets**.

---

## 🏗️ Архитектура проекта

```
GitHub
  ↓
Cloudflare Workers (Python Runtime via Pyodide / workerd)
  ↓
FastAPI ASGI Entrypoint (src/worker.py)
  ↓
Supabase (PostgreSQL Database + Storage)
  ↓
Cloudflare Workers Static Assets (public/)
```

* **Backend / API**: FastAPI на Cloudflare Python Workers (`src/worker.py` -> `Default = asgi.entrypoint(app)`).
* **База данных**: PostgreSQL на Supabase (драйвер `pg8000`) в production, SQLite для локальной разработки.
* **Статика и фронтенд**: Cloudflare Workers Static Assets (`public/`).
* **Аутентификация**: JWT Bearer + HTTP-only cookies.
* **Хранилище загрузок**: Supabase Storage (`/storage/v1/object/public/uploads`) или локальная папка.

---

## 🌟 Основные возможности

1. **Каталог и фильтрация**: Живой поиск, фильтры по категориям, ценам, размерам, цветам, скидкам, наличию.
2. **Карточка товара**: Галерея фото, выбор размера/цвета, точные складские остатки, покупка в 1 клик.
3. **Корзина и оформление**: Подсчет скидок, шкала бесплатной доставки, синхронизация гостевой корзины, выбор способов доставки и оплаты.
4. **Личный кабинет (`/profile`)**: История заказов, список избранного (Wishlist), сохраненные адреса, смена пароля.
5. **Админ-панель (`/admin`)**: Аналитика дашборда, CRUD товаров и вариантов, управление категориями, заказами и статусами, модерация пользователей.
6. **SEO и мета-теги**: Schema.org, Open Graph, динамический `/robots.txt` и `/sitemap.xml` на основе `SITE_URL`.

---

## 📁 Структура проекта

```text
Female-Fabric/
├── app/                        # Основной исходный код FastAPI
│   ├── api/                    # API-роутеры (auth, products, cart, checkout, admin, etc.)
│   ├── core/                   # Безопасность, зависимости, сидинг данных
│   ├── models/                 # SQLAlchemy ORM модели
│   ├── schemas/                # Pydantic схемы
│   ├── static/                 # CSS, JS, изображения
│   ├── templates/              # HTML-шаблоны
│   ├── config.py               # Настройки приложения
│   ├── database.py             # Подключение к БД (SQLAlchemy)
│   └── main.py                 # FastAPI приложение
├── public/                     # Статические файлы для Cloudflare Workers Static Assets
├── src/
│   └── worker.py               # Cloudflare Worker ASGI Entrypoint
├── scripts/
│   └── init_db.py              # Скрипт инициализации и миграции базы данных
├── .env.example                # Шаблон переменных окружения
├── pyproject.toml              # Манифест зависимостей Cloudflare Python Workers
├── requirements.txt            # Зависимости для локального pip
├── wrangler.jsonc              # Конфигурация Cloudflare Wrangler
├── supabase-schema.sql         # SQL-схема для Supabase PostgreSQL
├── run.py                      # Локальный запуск через uvicorn
└── test_app.py                 # Автоматический тестовый набор
```

---

## 🚀 Быстрый старт

### ⚡ Самый простой способ (для Windows)

**1. Дважды кликните на `run-local.bat`**

Всё! Приложение откроется на http://localhost:8000

(Если батник требует доп. действий, см. `SETUP.md`)

### 📖 Подробнее

Полная пошаговая инструкция: **[SETUP.md](./SETUP.md)**

Там же:
- ✓ Как установить все программы
- ✓ Как запустить приложение
- ✓ Что делать если что-то не работает
- ✓ Как деплоить на Cloudflare

---

## 🧪 Запуск тестов

Для проверки работоспособности всех модулей, API, страниц и безопасности:

```bash
python test_app.py
```

---

## ☁️ Развертывание в Cloudflare Workers

### Краткая инструкция

1. **Установите инструменты** (см. `INSTALL_TOOLS.md`):
   - Node.js и npm
   - Wrangler CLI: `npm install -g wrangler`
   - uv (опционально): `pip install uv`

2. **Настройте Supabase** (подробнее в `SUPABASE_SETUP.md`):
   - Создайте проект на [supabase.com](https://supabase.com)
   - Выполните SQL из `supabase-schema.sql`
   - Получите Connection String (Session mode, порт 6543)

3. **Установите секреты Cloudflare**:
   ```bash
   wrangler login
   wrangler secret put SECRET_KEY
   wrangler secret put DATABASE_URL
   ```

4. **Деплой**:
   ```bash
   uv run pywrangler deploy
   # или
   wrangler deploy
   ```

**Подробная инструкция:** см. файлы `QUICKSTART.md` и `SUPABASE_SETUP.md`

---

## 🔑 Тестовые учетные записи

* **Администратор:**
  * **Email:** `admin@female-fabric.ru`
  * **Пароль:** `Admin123!`
* **Покупатель:**
  * **Email:** `user@female-fabric.ru`
  * **Пароль:** `User123!`

