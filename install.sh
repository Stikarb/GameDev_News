#!/bin/bash

# Очистка предыдущих сборок
rm -rf dist build news_parser news_parser.spec 2>/dev/null

# Создание виртуального окружения
python3 -m venv venv || { echo "Ошибка создания виртуального окружения"; exit 1; }
source venv/bin/activate

# Установка зависимостей
pip install requests pyinstaller --quiet || { 
    echo "Ошибка установки зависимостей"
    deactivate
    exit 1
}

# Сборка исполняемого файла
pyinstaller --onefile --noconsole \
    --add-data "src/template.html:." \
    --hidden-import=requests \
    src/news_parser.py || {
    echo "Ошибка сборки"
    deactivate
    exit 1
}

# Копирование результата
cp dist/news_parser . || echo "Предупреждение: не удалось скопировать бинарник"

deactivate
echo "Установка завершена. Для запуска выполните: ./news_parser"
