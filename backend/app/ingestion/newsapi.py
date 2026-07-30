import requests
from app.config import settings

BASE_URL = "https://newsapi.org/v2/everything"


def fetch_news(query: str, page_size: int = 10):
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": settings.NEWS_API_KEY,
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        print("NewsAPI Error:", response.text)
        return []

    data = response.json()

    articles = []

    for article in data.get("articles", []):

        articles.append({
            "title": article.get("title", ""),
            "source": article.get("source", {}).get("name", "NewsAPI"),
            "url": article.get("url", ""),
            "published_at": article.get("publishedAt", ""),
            "clean_text": article.get("content") or article.get("description") or ""
        })

    return articles