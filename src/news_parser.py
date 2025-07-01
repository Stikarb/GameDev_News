import requests
import datetime
import webbrowser
import os
import time
import sys

def parse_reddit_indiedev():
    try:
        url = "https://www.reddit.com/r/IndieDev/hot.json?limit=10"
        headers = {"User-Agent": "GameDevNews/1.0"}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        videos = []
        feedbacks = []
        
        for post in data['data']['children']:
            p = post['data']
            flair = p.get('link_flair_text', '')
            
            if flair == "Video" and not p['stickied']:
                videos.append({
                    "source": "r/IndieDev",
                    "title": p['title'],
                    "url": "https://reddit.com" + p['permalink'],
                    "date": datetime.datetime.fromtimestamp(p['created_utc']).strftime('%d.%m.%Y'),
                    "type": "video"
                })
            elif flair == "Feedback?" and not p['stickied']:
                feedbacks.append({
                    "source": "r/IndieDev",
                    "title": p['title'],
                    "url": "https://reddit.com" + p['permalink'],
                    "date": datetime.datetime.fromtimestamp(p['created_utc']).strftime('%d.%m.%Y'),
                    "type": "feedback"
                })
                
        return videos[:5], feedbacks[:5]
    
    except Exception:
        return [], []

def parse_reddit_indiegames():
    try:
        url = "https://www.reddit.com/r/indiegames/hot.json?limit=15"
        headers = {"User-Agent": "GameDevNews/1.0"}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        promotions = []
        
        for post in data['data']['children']:
            p = post['data']
            flair = p.get('link_flair_text', '')
            
            if flair == "Promotion" and not p['stickied']:
                promotions.append({
                    "source": "r/indiegames",
                    "title": p['title'],
                    "url": "https://reddit.com" + p['permalink'],
                    "date": datetime.datetime.fromtimestamp(p['created_utc']).strftime('%d.%m.%Y'),
                    "type": "promotion"
                })
                
        return promotions[:5]
    
    except Exception:
        return []

def load_css():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        css_path = os.path.join(base_path, 'src', 'style.css')
    else:
        base_path = os.path.dirname(__file__)
        css_path = os.path.join(base_path, 'style.css')
    
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return "body { background: #1a1a2e; color: #e6e6e6; }"

def generate_html(videos, feedbacks, promotions):
    timestamp = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    css_content = load_css()
    
    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вестник игростроя</title>
    <style>{css_content}</style>
</head>
<body>
    <header>
        <h1>Вестник игростроя</h1>
        <div class="subtitle">Свежие материалы прямо от разработчиков</div>
    </header>
    
    <div class="timestamp">Обновлено: {timestamp}</div>
    
    <div class="category">Видео разработки</div>
    <div class="news-grid">
        {"".join(f'''
        <div class="news-item video">
            <div class="news-content">
                <h3><a href="{item["url"]}" target="_blank">{item["title"]}</a></h3>
                <div class="meta">
                    <div class="source">{item["source"]}</div>
                    <div class="date">{item["date"]}</div>
                </div>
            </div>
        </div>
        ''' for item in videos)}
    </div>
    
    <div class="category">Запросы фидбэка</div>
    <div class="news-grid">
        {"".join(f'''
        <div class="news-item feedback">
            <div class="news-content">
                <h3><a href="{item["url"]}" target="_blank">{item["title"]}</a></h3>
                <div class="meta">
                    <div class="source">{item["source"]}</div>
                    <div class="date">{item["date"]}</div>
                </div>
            </div>
        </div>
        ''' for item in feedbacks)}
    </div>
    
    <div class="category">Промо проектов</div>
    <div class="news-grid">
        {"".join(f'''
        <div class="news-item promotion">
            <div class="news-content">
                <h3><a href="{item["url"]}" target="_blank">{item["title"]}</a></h3>
                <div class="meta">
                    <div class="source">{item["source"]}</div>
                    <div class="date">{item["date"]}</div>
                </div>
            </div>
        </div>
        ''' for item in promotions)}
    </div>
    
    <footer>
        Сгенерировано автоматически • Вестник игростроя • v4.0
    </footer>
</body>
</html>"""
    
    with open("game_news.html", "w", encoding="utf-8") as f:
        f.write(html)
    return os.path.abspath("game_news.html")

if __name__ == "__main__":
    start_time = time.time()
    
    videos, feedbacks = parse_reddit_indiedev()
    promotions = parse_reddit_indiegames()
    
    report_path = generate_html(videos, feedbacks, promotions)
    
    elapsed = time.time() - start_time
    print(f"Отчёт готов за {elapsed:.2f} сек")
    print(f"Видео: {len(videos)} | Фидбэк: {len(feedbacks)} | Промо: {len(promotions)}")
    webbrowser.open(report_path)
