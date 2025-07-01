#!/bin/bash
source venv/bin/activate
pyinstaller --onefile --noconsole \
    --add-data "src/style.css:src" \
    --hidden-import=requests \
    src/news_parser.py
cp dist/news_parser .
echo "✅ Готово! Запуск: ./news_parser"
