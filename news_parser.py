import requests
from bs4 import BeautifulSoup
import datetime
import json
import webbrowser
import os

def get_reddit_news():
    """Парсим r/gamedev"""
    try:
        url = "https://www.reddit.com/r/gamedev/hot.json?limit=5"
        headers = {"User-Agent": "GameDevNews/1.0"}
        data = requests.get(url, headers=headers).json()
        
        news = []
        for post in data["data"]["children"]:
            if post["data"]["stickied"]: continue
            news.append({
                "title": post["data"]["title"],
                "url": "https://reddit.com" + post["data"]["permalink"],
                "date": datetime.datetime.fromtimestamp(post["data"]["created_utc"]).strftime("%d.%m.%Y"),
                "source": "Reddit r/gamedev"
            })
        return news
    except Exception as e:
        print(f"🚨 Ошибка Reddit: {e}")
        return []

def get_stopgame_news():
    """Парсим StopGame.ru"""
    try:
        url = "https://stopgame.ru/news"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        
        news = []
        for article in soup.select("div._card_1tbpr_1"):  # Селектор на 2025 год
            news.append({
                "title": article.select_one("h3._title_1tbpr_49").text.strip(),
                "url": "https://stopgame.ru" + article.find("a")["href"],
                "date": article.select_one("span._date_1tbpr_100").text.strip(),
                "source": "StopGame"
            })
        return news[:5]
    except Exception as e:
        print(f"🚨 Ошибка StopGame: {e}")
        return []

def save_html(news):
    """Генерируем HTML-отчёт"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Вестник игростроя</title>
        <style>
            body {{ font-family: Arial; max-width: 800px; margin: 0 auto; padding: 20px; }}
            h1 {{ color: #2c3e50; text-align: center; }}
            .news-item {{ margin: 15px 0; padding: 10px; border-radius: 5px; }}
            .stopgame {{ background: #e3f2fd; border-left: 4px solid #2196F3; }}
            .reddit {{ background: #fff8e1; border-left: 4px solid #ffc107; }}
            a {{ color: #1e88e5; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <h1>📰 Вестник игростроя</h1>
        <p>Собрано: {datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}</p>
    """
    
    for item in news:
        html += f"""
        <div class="news-item {item['source'].lower()}">
            <h3><a href="{item['url']}" target="_blank">{item['title']}</a></h3>
            <p><b>{item['source']}</b> | {item['date']}</p>
        </div>
        """
    
    html += "</body></html>"
    
    with open("game_news.html", "w", encoding="utf-8") as f:
        f.write(html)
    return "game_news.html"

if __name__ == "__main__":
    print("🔍 Ищем свежие новости...")
    news = get_stopgame_news() + get_reddit_news()
    news.sort(key=lambda x: x["date"], reverse=True)
    
    report = save_html(news)
    webbrowser.open(report)
    print(f"✅ Готово! Отчёт: {os.path.abspath(report)}")
