#!/bin/bash

echo "Выберите действие:"
echo "1) Удалить только временные файлы"
echo "2) Удалить весь проект"
read -rp "Введите номер [1-2]: " choice

case $choice in
    1)
        echo "Очистка временных файлов..."
        rm -rf venv dist build
        rm -f news_parser game_news.html news_parser.spec
        echo "Очистка завершена"
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
