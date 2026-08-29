@echo off
REM Запуск Female-Fabric локально

echo.
echo ========================================
echo   Female-Fabric - Локальный запуск
echo ========================================
echo.

REM Проверяем Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ОШИБКА: Python не найден!
    echo.
    echo Сначала запустите install.bat
    echo.
    pause
    exit /b 1
)

REM Проверяем requirements.txt
if not exist "requirements.txt" (
    echo ОШИБКА: requirements.txt не найден!
    pause
    exit /b 1
)

echo [1/3] Проверка зависимостей...
python -m pip install -r requirements.txt -q --disable-pip-version-check
if %errorLevel% neq 0 (
    echo ОШИБКА: Не удалось установить зависимости
    pause
    exit /b 1
)

echo [2/3] Проверка .env файла...
if not exist ".env" (
    echo ОШИБКА: .env файл не найден!
    echo.
    echo Скопируйте .env.example в .env и отредактируйте при необходимости
    pause
    exit /b 1
)

echo [3/3] Запуск сервера на http://localhost:8000...
echo.
echo ========================================
echo.

python run.py

if %errorLevel% neq 0 (
    echo.
    echo ОШИБКА: Сервер не запустился
    pause
    exit /b 1
)
