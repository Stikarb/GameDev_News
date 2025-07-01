import requests
from datetime import datetime, timedelta
import webbrowser
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

class RedditParser:
    def __init__(self):
        self.user_agent = "GameDevNewsParser/1.0"
        self.timeout = 15
        self.max_posts = 5
        self.min_post_age = 90  # дней

    def fetch_posts(self, subreddit, flair_type=None):
        try:
            params = {"limit": 25}
            if flair_type:
                params["flair"] = flair_type
            
            response = requests.get(
                f"https://www.reddit.com/r/{subreddit}/hot.json",
                headers={"User-Agent": self.user_agent},
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            posts = []
            cutoff_date = datetime.now() - timedelta(days=self.min_post_age)
            
            for post in response.json()["data"]["children"]:
                data = post["data"]
                if data["stickied"]:
                    continue
                
                post_date = datetime.fromtimestamp(data["created_utc"])
                if post_date < cutoff_date:
                    continue
                
                posts.append({
                    "title": data["title"],
                    "url": f"https://reddit.com{data['permalink']}",
                    "date": post_date.strftime("%d.%m.%Y"),
                    "source": f"r/{subreddit}",
                    "type": "video" if flair_type == "Video" else 
                           "feedback" if flair_type == "Feedback" else 
                           "promotion"
                })
                
                if len(posts) >= self.max_posts:
                    break
            
            return posts
        
        except Exception as error:
            print(f"Ошибка при обработке r/{subreddit}: {error}", file=sys.stderr)
            return []

def get_template_path():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        return os.path.join(base_path, 'src', 'template.html')
    else:
        return os.path.join(os.path.dirname(__file__), 'template.html')

def load_css():
    try:
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
            css_path = os.path.join(base_path, 'src', 'style.css')
        else:
            base_path = os.path.dirname(__file__)
            css_path = os.path.join(base_path, 'style.css')
        
        with open(css_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Ошибка загрузки CSS: {e}", file=sys.stderr)
        return "body { font-family: sans-serif; }"

def generate_report_content(data):
    html_content = []
    for category in data:
        html_content.append(f'<div class="category">{category["name"]}</div>')
        html_content.append('<div class="news-grid">')
        
        for item in category["items"]:
            html_content.append(f'''
            <div class="news-item {category["class"]}">
                <div class="news-content">
                    <h3><a href="{item["url"]}" target="_blank">{item["title"]}</a></h3>
                    <div class="meta">
                        <div class="source">{item["source"]}</div>
                        <div class="date">{item["date"]}</div>
                    </div>
                </div>
            </div>
            ''')
        
        html_content.append('</div>')
    
    return "\n".join(html_content)

def main():
    start_time = time.time()
    parser = RedditParser()
    
    with ThreadPoolExecutor() as executor:
        videos_future = executor.submit(parser.fetch_posts, "IndieDev", "Video")
        feedbacks_future = executor.submit(parser.fetch_posts, "IndieDev", "Feedback")
        promotions_future = executor.submit(parser.fetch_posts, "indiegames", "Promotion")
        
        videos = videos_future.result() or []
        feedbacks = feedbacks_future.result() or []
        promotions = promotions_future.result() or []
    
    report_data = [
        {
            "name": "Видео разработки", 
            "items": videos[:5],
            "class": "video"
        },
        {
            "name": "Запросы фидбэка",
            "items": feedbacks[:5],
            "class": "feedback"
        },
        {
            "name": "Промо проектов",
            "items": promotions[:5], 
            "class": "promotion"
        }
    ]
    
    try:
        with open(get_template_path(), 'r', encoding='utf-8') as file:
            template = file.read()
    except FileNotFoundError as e:
        print(f"Файл шаблона не найден: {e}", file=sys.stderr)
        sys.exit(1)
    
    final_html = template.replace("{{css}}", load_css()) \
                        .replace("{{timestamp}}", datetime.now().strftime("%d.%m.%Y %H:%M")) \
                        .replace("<!-- CONTENT_PLACEHOLDER -->", generate_report_content(report_data))
    
    with open("game_news.html", "w", encoding="utf-8") as file:
        file.write(final_html)
    
    elapsed = time.time() - start_time
    print(f"Отчёт сформирован за {elapsed:.2f} секунд")
    print(f"Статистика: Видео {len(videos)} | Фидбэк {len(feedbacks)} | Промо {len(promotions)}")
    
    webbrowser.open("game_news.html")

if __name__ == "__main__":
    main()
