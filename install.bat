@echo off
REM Создание изолированного окружения и сборка проекта
python -m venv venv
call venv\Scripts\activate.bat
pip install requests pyinstaller --quiet --no-warn-script-location

REM Сборка исполняемого файла с включением CSS
pyinstaller --onefile --noconsole ^
    --add-data "src/style.css;src" ^
    --hidden-import=requests ^
    src/news_parser.py

REM Копирование результата в корень проекта
copy dist\news_parser.exe . >nul

deactivate
echo Установка завершена. Запуск: news_parser.exe
