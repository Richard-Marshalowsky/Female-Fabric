# Female-Fabric Auto-Installer для Windows
# Скрипт скачает и установит все необходимые программы

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Female-Fabric Installer для Windows" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Функция для проверки установки программы
function Test-Command {
    param($Command)
    try {
        & $Command --version 2>&1 | Out-Null
        return $true
    } catch {
        return $false
    }
}

# 1. Проверка Python
Write-Host "[1/5] Проверка Python..." -ForegroundColor Yellow
if (Test-Command python) {
    $pythonVersion = python --version
    Write-Host "  ✓ $pythonVersion уже установлен" -ForegroundColor Green
} else {
    Write-Host "  ✗ Python не найден!" -ForegroundColor Red
    Write-Host "  📥 Скачиваю Python 3.11..." -ForegroundColor Yellow
    $pythonUrl = "https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe"
    $pythonInstaller = "$env:TEMP\python-installer.exe"
    Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller -ErrorAction SilentlyContinue
    if (Test-Path $pythonInstaller) {
        Write-Host "  ⚙️  Запускаю установщик Python..." -ForegroundColor Yellow
        & $pythonInstaller /quiet InstallAllUsers=1 PrependPath=1 | Wait-Process
        Remove-Item $pythonInstaller -ErrorAction SilentlyContinue
        Write-Host "  ✓ Python установлен" -ForegroundColor Green
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    } else {
        Write-Host "  ⚠️  Не удалось скачать Python. Скачайте вручную с https://python.org" -ForegroundColor Red
    }
}

# 2. Проверка Node.js
Write-Host ""
Write-Host "[2/5] Проверка Node.js..." -ForegroundColor Yellow
if (Test-Command node) {
    $nodeVersion = node --version
    Write-Host "  ✓ Node.js $nodeVersion уже установлен" -ForegroundColor Green
} else {
    Write-Host "  ✗ Node.js не найден!" -ForegroundColor Red
    Write-Host "  📥 Скачиваю Node.js LTS..." -ForegroundColor Yellow
    $nodeUrl = "https://nodejs.org/dist/v20.11.1/node-v20.11.1-x64.msi"
    $nodeInstaller = "$env:TEMP\node-installer.msi"
    try {
        Invoke-WebRequest -Uri $nodeUrl -OutFile $nodeInstaller -TimeoutSec 30 -ErrorAction SilentlyContinue
        if (Test-Path $nodeInstaller) {
            Write-Host "  ⚙️  Запускаю установщик Node.js..." -ForegroundColor Yellow
            & msiexec /i $nodeInstaller /quiet | Wait-Process
            Remove-Item $nodeInstaller -ErrorAction SilentlyContinue
            Write-Host "  ✓ Node.js установлен" -ForegroundColor Green
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        }
    } catch {
        Write-Host "  ⚠️  Не удалось скачать Node.js. Скачайте вручную с https://nodejs.org" -ForegroundColor Red
    }
}

# 3. Установка pip пакетов
Write-Host ""
Write-Host "[3/5] Установка Python зависимостей..." -ForegroundColor Yellow
Write-Host "  📦 Устанавливаю пакеты из requirements.txt..." -ForegroundColor Cyan
python -m pip install --upgrade pip -q
python -m pip install -r requirements.txt -q
Write-Host "  ✓ Python зависимости установлены" -ForegroundColor Green

# 4. Установка Wrangler
Write-Host ""
Write-Host "[4/5] Установка Wrangler (Cloudflare CLI)..." -ForegroundColor Yellow
if (Test-Command wrangler) {
    $wranglerVersion = wrangler --version
    Write-Host "  ✓ $wranglerVersion уже установлен" -ForegroundColor Green
} else {
    Write-Host "  📦 Устанавливаю Wrangler через npm..." -ForegroundColor Cyan
    npm install -g wrangler -q
    Write-Host "  ✓ Wrangler установлен" -ForegroundColor Green
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# 5. Установка uv
Write-Host ""
Write-Host "[5/5] Установка uv (Python Package Manager)..." -ForegroundColor Yellow
if (Test-Command uv) {
    $uvVersion = uv --version
    Write-Host "  ✓ $uvVersion уже установлен" -ForegroundColor Green
} else {
    Write-Host "  📦 Устанавливаю uv..." -ForegroundColor Cyan
    python -m pip install uv -q
    Write-Host "  ✓ uv установлен" -ForegroundColor Green
}

# Итоговая проверка
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✓ Установка завершена!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Финальная проверка всех компонентов
Write-Host "Проверка установленных компонентов:" -ForegroundColor Cyan
Write-Host ""

$components = @(
    ("Python", "python"),
    ("Node.js", "node"),
    ("npm", "npm"),
    ("Wrangler", "wrangler"),
    ("uv", "uv")
)

foreach ($comp in $components) {
    $name = $comp[0]
    $cmd = $comp[1]
    if (Test-Command $cmd) {
        $version = & $cmd --version 2>&1
        Write-Host "  ✓ $name : $version" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $name : не установлен" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🚀 Готово! Можешь запускать приложение:" -ForegroundColor Green
Write-Host ""
Write-Host "   Локальный запуск:" -ForegroundColor Cyan
Write-Host "   python run.py" -ForegroundColor White
Write-Host ""
Write-Host "   Запуск тестов:" -ForegroundColor Cyan
Write-Host "   python test_app.py" -ForegroundColor White
Write-Host ""
Write-Host "   Для деплоя на Cloudflare Workers см. QUICKSTART.md" -ForegroundColor Yellow
Write-Host ""
