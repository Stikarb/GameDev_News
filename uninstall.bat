@echo off
set /p choice="Выберите действие [1-2]: 
1. Удалить только временные файлы
2. Удалить весь проект
"

if "%choice%"=="1" (
    echo Очистка временных файлов...
    rmdir /s /q venv 2>nul
    rmdir /s /q dist 2>nul
    rmdir /s /q build 2>nul
    del news_parser.exe 2>nul
    del game_news.html 2>nul
    del news_parser.spec 2>nul
    echo Временные файлы удалены
) else if "%choice%"=="2" (
    echo Полное удаление проекта...
    set "project_path=%cd%"
    cd ..
    rmdir /s /q "%project_path%"
    echo Проект удален
) else (
    echo Неверный выбор
)
