import requests
from datetime import datetime, timedelta
import webbrowser
import os
import sys
from concurrent.futures import ThreadPoolExecutor

class RedditParser:
    def __init__(self):
        self.user_agent = "RedditParser/1.0"
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
                    "source": f"r/{subreddit}"
                })
                
                if len(posts) >= self.max_posts:
                    break
            
            return posts
        
        except Exception as error:
            print(f"Ошибка при обработке r/{subreddit}: {error}", file=sys.stderr)
            return []

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
    parser = RedditParser()
    
    with ThreadPoolExecutor() as executor:
        futures = {
            "videos": executor.submit(parser.fetch_posts, "IndieDev", "Video"),
            "feedbacks": executor.submit(parser.fetch_posts, "IndieDev", "Feedback"),
            "promotions": executor.submit(parser.fetch_posts, "indiegames", "Promotion")
        }
        
        results = {key: future.result() for key, future in futures.items()}
    
    report_data = [
        {
            "name": "Видео разработки", 
            "items": results["videos"],
            "class": "video"
        },
        {
            "name": "Запросы фидбэка",
            "items": results["feedbacks"],
            "class": "feedback"
        },
        {
            "name": "Промо проектов",
            "items": results["promotions"], 
            "class": "promotion"
        }
    ]
    
    with open("template.html", "r", encoding="utf-8") as file:
        template = file.read()
    
    final_html = template.replace(
        "<!-- CONTENT_PLACEHOLDER -->", 
        generate_report_content(report_data)
    )
    
    with open("game_news.html", "w", encoding="utf-8") as file:
        file.write(final_html)
    
    webbrowser.open("game_news.html")

if __name__ == "__main__":
    main()
