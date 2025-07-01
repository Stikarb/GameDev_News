#!/bin/bash

# Создаем виртуальное окружение
python3 -m venv venv

# Активируем виртуальное окружение
source venv/bin/activate

# Устанавливаем зависимости
pip install requests pyinstaller

# Собираем исполняемый файл
pyinstaller --onefile --noconsole \
    --add-data "src/style.css:src" \
    --hidden-import=requests \
    src/news_parser.py

# Копируем исполняемый файл
cp dist/news_parser .

# Деактивируем виртуальное окружение
deactivate

# Запускаем программу
./news_parser
