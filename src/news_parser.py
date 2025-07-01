import requests
import datetime
import webbrowser
import os
import time
import sys
from concurrent.futures import ThreadPoolExecutor

def fetch_reddit_posts(subreddit, limit=25, flair_filter=None):
    """Получение постов с Reddit с возможностью фильтрации по flair"""
    try:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
        headers = {"User-Agent": "GameDevNews/1.0"}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        posts = []
        for post in data['data']['children']:
            p = post['data']
            if p['stickied']:
                continue
                
            # Проверка соответствия flair фильтру
            post_flair = p.get('link_flair_text', '')
            if flair_filter and post_flair != flair_filter:
                continue
                
            # Фильтр по дате (не старше 3 месяцев)
            post_date = datetime.datetime.fromtimestamp(p['created_utc'])
            if (datetime.datetime.now() - post_date).days > 90:
                continue
                
            posts.append({
                "title": p['title'],
                "url": "https://reddit.com" + p['permalink'],
                "date": post_date.strftime('%d.%m.%Y'),
                "source": f"r/{subreddit}",
                "type": "video" if flair_filter == "Video" else 
                       "feedback" if flair_filter == "Feedback?" else 
                       "promotion"
            })
            if len(posts) >= 5:  # Нам нужно максимум 5 постов
                break
                
        return posts
        
    except Exception as e:
        print(f"Ошибка при получении данных из r/{subreddit}: {str(e)}", file=sys.stderr)
        return []

def load_css():
    """Загрузка CSS с учетом режима выполнения (исходник или exe)"""
    try:
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
            css_path = os.path.join(base_path, 'src', 'style.css')
        else:
            base_path = os.path.dirname(__file__)
            css_path = os.path.join(base_path, 'style.css')
            
        with open(css_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return "body { font-family: sans-serif; }"

def generate_html(videos, feedbacks, promotions):
    """Генерация HTML отчета с гарантированными 5 элементами в каждой секции"""
    timestamp = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    
    # Дополняем списки до 5 элементов, если нужно
    for lst in [videos, feedbacks, promotions]:
        while len(lst) < 5:
            lst.append({
                "title": "Материал не найден",
                "url": "#",
                "date": "Н/Д",
                "source": "Система",
                "type": lst[0]["type"] if lst else "promotion"
            })
    
    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вестник игростроя</title>
    <style>{load_css()}</style>
</head>
<body>
    <header>
        <h1>Вестник игростроя</h1>
        <div class="subtitle">Последние материалы для разработчиков игр</div>
    </header>
    
    <div class="timestamp">Обновлено: {timestamp}</div>
    
    <div class="category">Видео разработки</div>
    <div class="news-grid">
        {''.join(f'''
        <div class="news-item video">
            <div class="news-content">
                <h3><a href="{item['url']}" target="_blank">{item['title']}</a></h3>
                <div class="meta">
                    <div class="source">{item['source']}</div>
                    <div class="date">{item['date']}</div>
                </div>
            </div>
        </div>
        ''' for item in videos[:5])}
    </div>
    
    <div class="category">Запросы фидбэка</div>
    <div class="news-grid">
        {''.join(f'''
        <div class="news-item feedback">
            <div class="news-content">
                <h3><a href="{item['url']}" target="_blank">{item['title']}</a></h3>
                <div class="meta">
                    <div class="source">{item['source']}</div>
                    <div class="date">{item['date']}</div>
                </div>
            </div>
        </div>
        ''' for item in feedbacks[:5])}
    </div>
    
    <div class="category">Промо проектов</div>
    <div class="news-grid">
        {''.join(f'''
        <div class="news-item promotion">
            <div class="news-content">
                <h3><a href="{item['url']}" target="_blank">{item['title']}</a></h3>
                <div class="meta">
                    <div class="source">{item['source']}</div>
                    <div class="date">{item['date']}</div>
                </div>
            </div>
        </div>
        ''' for item in promotions[:5])}
    </div>
    
    <footer>
        <div class="version">Вестник игростроя • v5.1</div>
    </footer>
</body>
</html>"""
    
    with open("game_news.html", "w", encoding="utf-8") as f:
        f.write(html)
    return os.path.abspath("game_news.html")

def main():
    start_time = time.time()
    
    # Параллельный сбор данных
    with ThreadPoolExecutor() as executor:
        videos_future = executor.submit(fetch_reddit_posts, "IndieDev", 25, "Video")
        feedbacks_future = executor.submit(fetch_reddit_posts, "IndieDev", 25, "Feedback?")
        promotions_future = executor.submit(fetch_reddit_posts, "indiegames", 25, "Promotion")
        
        videos = videos_future.result()
        feedbacks = feedbacks_future.result()
        promotions = promotions_future.result()
    
    report_path = generate_html(videos, feedbacks, promotions)
    
    elapsed = time.time() - start_time
    print(f"Отчёт сформирован за {elapsed:.2f} секунд")
    print(f"Статистика: Видео {len(videos)} | Фидбэк {len(feedbacks)} | Промо {len(promotions)}")
    
    webbrowser.open(report_path)

if __name__ == "__main__":
    main()
