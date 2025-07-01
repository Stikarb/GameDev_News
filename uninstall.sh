#!/bin/bash

echo "Выберите действие:"
echo "1. Удалить временные файлы (оставить проект)"
echo "2. Полностью удалить проект"
read -rp "Введите номер [1-2]: " choice

case $choice in
    1)
        echo "Удаление временных файлов..."
        [ -d "venv" ] && rm -rf venv
        [ -d "dist" ] && rm -rf dist
        [ -d "build" ] && rm -rf build
        [ -f "news_parser" ] && rm -f news_parser
        [ -f "news_parser.spec" ] && rm -f news_parser.spec
        [ -f "game_news.html" ] && rm -f game_news.html
        echo "Временные файлы удалены"
        ;;
    2)
        echo "Полное удаление проекта..."
        cd ..
        rm -rf -- "$(basename "$PWD")"
        echo "Проект удален"
        ;;
    *)
        echo "Неверный выбор"
        exit 1
        ;;
esac
