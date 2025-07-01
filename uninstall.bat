@echo off
setlocal enabledelayedexpansion

echo Выберите действие:
echo 1. Удалить только временные файлы
echo 2. Удалить весь проект
set /p choice="Введите номер [1-2]: "

if "!choice!"=="1" (
    echo Удаление временных файлов...
    if exist venv rmdir /s /q venv
    if exist dist rmdir /s /q dist
    if exist build rmdir /s /q build
    del news_parser.exe 2>nul
    del game_news.html 2>nul
    del news_parser.spec 2>nul
    echo Временные файлы удалены
) else if "!choice!"=="2" (
    echo Полное удаление проекта...
    set "project_dir=%~dp0"
    cd /d "%project_dir%"
    cd ..
    rmdir /s /q "%project_dir%"
    echo Проект полностью удален
) else (
    echo Неверный выбор
    exit /b 1
)

endlocal
