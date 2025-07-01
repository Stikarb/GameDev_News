import requests
from datetime import datetime, timedelta
import webbrowser
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

class RedditParser:
    """Основной класс для парсинга данных с Reddit"""
    
    def __init__(self):
        # Настройки парсера
        self.user_agent = "GameDevNewsParser/1.0"
        self.timeout = 15  # Таймаут запроса в секундах
        self.max_posts = 5  # Максимальное количество постов на категорию
        self.min_post_age = 90  # Минимальный возраст постов в днях

    def fetch_posts(self, subreddit, flair_type=None):
        """Получение постов из указанного сабреддита"""
        try:
            # Параметры запроса
            params = {"limit": 25}
            if flair_type:
                params["flair"] = flair_type
            
            # Выполнение запроса
            response = requests.get(
                f"https://www.reddit.com/r/{subreddit}/hot.json",
                headers={"User-Agent": self.user_agent},
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()  # Проверка на ошибки HTTP
            
            # Фильтрация постов
            posts = []
            cutoff_date = datetime.now() - timedelta(days=self.min_post_age)
            
            for post in response.json()["data"]["children"]:
                data = post["data"]
                
                # Пропуск закрепленных постов
                if data["stickied"]:
                    continue
                
                # Проверка даты поста
                post_date = datetime.fromtimestamp(data["created_utc"])
                if post_date < cutoff_date:
                    continue
                
                # Формирование данных поста
                posts.append({
                    "title": data["title"],
                    "url": f"https://reddit.com{data['permalink']}",
                    "date": post_date.strftime("%d.%m.%Y"),
                    "source": f"r/{subreddit}",
                    "type": flair_type.lower() if flair_type else "general"
                })
                
                # Ограничение на количество постов
                if len(posts) >= self.max_posts:
                    break
            
            return posts
        
        except Exception as error:
            # Логирование ошибок
            print(f"Ошибка при получении данных из r/{subreddit}: {error}", file=sys.stderr)
            return []

def get_resource_path(relative_path):
    """Получение абсолютного пути к ресурсу"""
    # Режим исполнения: собранный exe
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    # Режим исполнения: скрипт Python
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def load_template():
    """Загрузка HTML шаблона"""
    try:
        template_path = get_resource_path('template.html')
        with open(template_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Ошибка загрузки шаблона: {e}", file=sys.stderr)
        sys.exit(1)

def generate_content(data):
    """Генерация HTML контента для отчета"""
    content = []
    for category in data:
        # Заголовок категории
        content.append(f'<div class="category">{category["name"]}</div>')
        content.append('<div class="news-grid">')
        
        # Посты в категории
        for item in category["items"]:
            content.append(f'''
            <div class="news-item {item["type"]}">
                <div class="news-content">
                    <h3><a href="{item["url"]}" target="_blank">{item["title"]}</a></h3>
                    <div class="meta">
                        <div class="source">{item["source"]}</div>
                        <div class="date">{item["date"]}</div>
                    </div>
                </div>
            </div>
            ''')
        
        content.append('</div>')
    
    return '\n'.join(content)

def main():
    """Основная функция программы"""
    start_time = time.time()
    parser = RedditParser()
    
    # Параллельный сбор данных
    with ThreadPoolExecutor(max_workers=3) as executor:
        videos_task = executor.submit(parser.fetch_posts, "IndieDev", "Video")
        feedbacks_task = executor.submit(parser.fetch_posts, "IndieDev", "Feedback")
        promotions_task = executor.submit(parser.fetch_posts, "indiegames", "Promotion")
        
        videos = videos_task.result() or []
        feedbacks = feedbacks_task.result() or []
        promotions = promotions_task.result() or []
    
    # Подготовка данных для отчета
    report_data = [
        {
            "name": "Видео разработки", 
            "items": videos
        },
        {
            "name": "Запросы фидбэка",
            "items": feedbacks
        },
        {
            "name": "Промо проектов",
            "items": promotions
        }
    ]
    
    # Генерация HTML
    template = load_template()
    html_content = generate_content(report_data)
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M")
    html_report = template.replace("{{content}}", html_content) \
                         .replace("{{timestamp}}", timestamp)
    
    # Сохранение отчета
    output_path = os.path.abspath("game_news.html")
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(html_report)
    
    # Статистика выполнения
    elapsed = time.time() - start_time
    print(f"Отчет сгенерирован за {elapsed:.2f} секунд")
    print(f"Видео: {len(videos)} | Фидбэк: {len(feedbacks)} | Промо: {len(promotions)}")
    
    # Открытие в браузере
    webbrowser.open(output_path)

if __name__ == "__main__":
    main()
