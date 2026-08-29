# Female-Fabric - Локальный запуск
# Запустите: powershell -ExecutionPolicy Bypass -File run-local.ps1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Female-Fabric - Локальный запуск" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Проверка Python
Write-Host "[1/3] Проверка Python..." -ForegroundColor Yellow
try {
    python --version | Out-Null
    $pythonVersion = python --version
    Write-Host "  ✓ $pythonVersion найден" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python не найден!" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Сначала запустите install.bat" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

# Проверка .env
Write-Host ""
Write-Host "[2/3] Проверка конфигурации..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Write-Host "  ✗ .env файл не найден!" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Скопируйте .env.example в .env:" -ForegroundColor Yellow
    Write-Host "  Copy-Item .env.example .env" -ForegroundColor White
    Write-Host ""
    pause
    exit 1
}
Write-Host "  ✓ .env найден" -ForegroundColor Green

# Установка зависимостей
Write-Host ""
Write-Host "[3/3] Установка зависимостей..." -ForegroundColor Yellow
python -m pip install -r requirements.txt -q --disable-pip-version-check
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ✗ Ошибка при установке зависимостей" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "  ✓ Зависимости установлены" -ForegroundColor Green

# Запуск сервера
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  🚀 Запуск сервера..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Откройте в браузере:" -ForegroundColor Cyan
Write-Host "  📱 Приложение:      http://localhost:8000" -ForegroundColor White
Write-Host "  📚 API документация: http://localhost:8000/docs" -ForegroundColor White
Write-Host "  🎛️  Админ панель:     http://localhost:8000/admin" -ForegroundColor White
Write-Host ""
Write-Host "Тестовые учетные записи:" -ForegroundColor Cyan
Write-Host "  📧 Админ:      admin@female-fabric.ru / Admin123!" -ForegroundColor White
Write-Host "  👤 Пользователь: user@female-fabric.ru / User123!" -ForegroundColor White
Write-Host ""
Write-Host "Нажмите Ctrl+C для остановки сервера" -ForegroundColor Yellow
Write-Host ""

python run.py
