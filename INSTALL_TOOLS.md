# 🛠️ Установка инструментов для деплоя на Cloudflare Workers

## Что нужно установить

1. **Node.js** — для Wrangler CLI
2. **Wrangler** — CLI для работы с Cloudflare Workers
3. **uv** (опционально) — современный Python package manager

---

## Установка Node.js (Windows)

### Вариант 1: Через официальный установщик

1. Скачайте установщик с [nodejs.org](https://nodejs.org/)
2. Выберите **LTS версию** (рекомендуется)
3. Запустите установщик и следуйте инструкциям
4. Перезапустите PowerShell/CMD после установки

### Вариант 2: Через Chocolatey

```powershell
choco install nodejs-lts
```

### Проверка установки

```powershell
node --version
npm --version
```

Должны появиться версии (например, `v20.11.0` и `10.2.4`)

---

## Установка Wrangler

После установки Node.js:

```powershell
npm install -g wrangler
```

### Проверка установки

```powershell
wrangler --version
```

### Авторизация в Cloudflare

```powershell
wrangler login
```

Откроется браузер для авторизации. После успешной авторизации можете закрыть окно браузера.

---

## Установка uv (опционально, но рекомендуется)

`uv` — это быстрый package manager для Python, который упрощает работу с Cloudflare Python Workers.

### Вариант 1: Через pip

```powershell
pip install uv
```

### Вариант 2: Через PowerShell скрипт (рекомендуется)

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Проверка установки

```powershell
uv --version
```

---

## Быстрая проверка всех инструментов

Запустите эти команды чтобы убедиться что все установлено:

```powershell
# Python
python --version

# pip
pip --version

# Node.js
node --version

# npm
npm --version

# Wrangler
wrangler --version

# uv (опционально)
uv --version
```

---

## Альтернативные инструменты

### pywrangler (входит в uv)

После установки `uv`, `pywrangler` становится доступен автоматически:

```powershell
uv run pywrangler --help
```

---

## Что делать дальше?

После установки всех инструментов:

1. Вернитесь к файлу `QUICKSTART.md`
2. Следуйте инструкциям по деплою на Cloudflare Workers
3. Настройте Supabase согласно `SUPABASE_SETUP.md`

---

## Troubleshooting

### npm команды не работают

- Перезапустите PowerShell/CMD после установки Node.js
- Убедитесь что Node.js добавлен в PATH (обычно автоматически)

### wrangler команда не найдена

Попробуйте:
```powershell
npx wrangler --version
```

Если работает через `npx`, используйте `npx wrangler` вместо просто `wrangler`.

### uv не устанавливается через pip

1. Обновите pip: `python -m pip install --upgrade pip`
2. Попробуйте PowerShell скрипт установки
3. Или скачайте напрямую с [GitHub](https://github.com/astral-sh/uv/releases)

### Ошибки прав доступа при установке глобальных пакетов

Запустите PowerShell **от имени администратора** и повторите установку.

---

## Полезные ссылки

- [Node.js официальный сайт](https://nodejs.org/)
- [Cloudflare Workers документация](https://developers.cloudflare.com/workers/)
- [Wrangler CLI документация](https://developers.cloudflare.com/workers/wrangler/)
- [uv документация](https://docs.astral.sh/uv/)
- [Python Workers документация](https://developers.cloudflare.com/workers/languages/python/)
