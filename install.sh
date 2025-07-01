#!/bin/bash

# Проверка доступности Python
if ! command -v python3 &> /dev/null; then
    echo "Ошибка: Python3 не установлен"
    exit 1
fi

# Создание виртуального окружения
python3 -m venv venv || { echo "Не удалось создать venv"; exit 1; }

# Активация окружения
source venv/bin/activate

# Установка зависимостей
pip install requests pyinstaller --quiet || { echo "Ошибка установки зависимостей"; deactivate; exit 1; }

# Сборка исполняемого файла
pyinstaller --onefile --noconsole \
    --add-data "src/style.css:src" \
    --hidden-import=requests \
    src/news_parser.py || { echo "Ошибка сборки"; deactivate; exit 1; }

# Копирование результата
cp dist/news_parser . || echo "Предупреждение: не удалось скопировать бинарник"

deactivate
echo "Установка завершена. Запуск: ./news_parser"
