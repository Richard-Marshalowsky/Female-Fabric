@echo off
REM Female-Fabric Auto-Installer для Windows
REM Запускает PowerShell скрипт установки

echo.
echo ========================================
echo   Female-Fabric Installer для Windows
echo ========================================
echo.

REM Проверяем права администратора
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ОШИБКА: Этот скрипт требует прав администратора!
    echo.
    echo Пожалуйста:
    echo   1. Откройте "Командная строка" от имени администратора
    echo   2. Перейдите в папку проекта
    echo   3. Запустите этот файл еще раз
    echo.
    pause
    exit /b 1
)

REM Проверяем PowerShell
powershell -Command "Write-Host 'PowerShell найден'" >nul 2>&1
if %errorLevel% neq 0 (
    echo ОШИБКА: PowerShell не найден!
    pause
    exit /b 1
)

REM Запускаем PowerShell скрипт
echo Запускаю скрипт установки...
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1"

if %errorLevel% equ 0 (
    echo.
    echo ========================================
    echo   Установка успешно завершена!
    echo ========================================
    echo.
) else (
    echo.
    echo ОШИБКА: Произошла ошибка при установке
    echo.
)

pause
