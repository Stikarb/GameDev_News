#!/bin/bash

echo "Выберите действие:"
echo "1. Удалить только временные файлы"
echo "2. Удалить весь проект"
read -rp "Введите номер [1-2]: " choice

case $choice in
    1)
        echo "Очистка временных файлов..."
        [ -d "venv" ] && rm -rf venv
        [ -d "dist" ] && rm -rf dist
        [ -d "build" ] && rm -rf build
        [ -f "news_parser" ] && rm -f news_parser
        [ -f "game_news.html" ] && rm -f game_news.html
        [ -f "news_parser.spec" ] && rm -f news_parser.spec
        echo "Временные файлы удалены"
        ;;
    2)
        echo "Полное удаление проекта..."
        cd ..
        rm -rf -- "$(basename "$OLDPWD")"
        echo "Проект полностью удален"
        ;;
    *)
        echo "Неверный выбор"
        exit 1
        ;;
esac
