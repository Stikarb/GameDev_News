@echo off
set /p choice="Вы хотите удалить только временные файлы (1) или весь проект (2)? "

if "%choice%"=="1" (
    echo Удаление временных файлов...
    rmdir /s /q venv
    rmdir /s /q dist
    rmdir /s /q build
    del news_parser.exe 2>nul
    del game_news.html 2>nul
    del news_parser.spec 2>nul
) else if "%choice%"=="2" (
    echo Удаление всего проекта...
    set "folder=%cd%"
    cd ..
    rmdir /s /q "%folder%"
) else (
    echo Неверный выбор.
)
