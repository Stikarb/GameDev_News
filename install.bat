@echo off
setlocal

:: Очистка предыдущих сборок
rmdir /s /q dist 2>nul
rmdir /s /q build 2>nul
del news_parser.exe 2>nul
del news_parser.spec 2>nul

:: Создание виртуального окружения
python -m venv venv || (echo Ошибка создания venv && exit /b 1)
call venv\Scripts\activate.bat || (echo Ошибка активации venv && exit /b 1)

:: Установка зависимостей
pip install requests pyinstaller --quiet || (
    echo Ошибка установки пакетов
    deactivate
    exit /b 1
)

:: Сборка исполняемого файла
pyinstaller --onefile --noconsole ^
    --add-data "src/style.css;src" ^
    --add-data "src/template.html;src" ^
    --hidden-import=requests ^
    src/news_parser.py || (
    echo Ошибка сборки
    deactivate
    exit /b 1
)

:: Копирование результата
copy dist\news_parser.exe . >nul || echo Предупреждение: не удалось скопировать файл

deactivate
echo Установка завершена. Запуск: news_parser.exe
endlocal
