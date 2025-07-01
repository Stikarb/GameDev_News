#!/bin/bash

echo "Вы хотите удалить только временные файлы (1) или весь проект (2)?"
read -p "Введите 1 или 2: " choice

if [ "$choice" = "1" ]; then
    echo "Удаление временных файлов..."
    rm -rf venv
    rm -rf dist
    rm -rf build
    rm -f news_parser
    rm -f game_news.html
    rm -f news_parser.spec
elif [ "$choice" = "2" ]; then
    echo "Удаление всего проекта..."
    cd ..
    rm -rf "$(basename "$PWD")"
else
    echo "Неверный выбор."
fi
