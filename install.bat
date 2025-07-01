@echo off
python -m venv venv
call venv\Scripts\activate.bat
pip install requests pyinstaller
pyinstaller --onefile --noconsole --add-data "src/style.css;src" --hidden-import=requests src/news_parser.py
copy dist\news_parser.exe .
deactivate
echo Установка завершена. Запуск: news_parser.exe
