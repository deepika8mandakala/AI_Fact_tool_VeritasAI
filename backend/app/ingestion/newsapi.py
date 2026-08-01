import requests
from newspaper import Article

from app.config import settings

BASE_URL = "https://newsapi.org/v2/everything"


def fetch_article(url: str):

    try:

        article = Article(url)

        article.download()

        article.parse()

        text = article.text.strip()

        if len(text) > 200:
            return text

    except Exception:
        pass

    return ""


def fetch_news(query: str, page_size: int = 10):

    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": settings.NEWS_API_KEY,
    }

    response = requests.get(
        BASE_URL,
        params=params
    )

    if response.status_code != 200:

        print("NewsAPI Error:", response.text)

        return []

    data = response.json()

    articles = []

    for article in data.get("articles", []):

        full_text = fetch_article(
            article.get("url", "")
        )

        if not full_text:

            full_text = (
                article.get("content")
                or article.get("description")
                or ""
            )

        articles.append(
            {
                "title": article.get("title", ""),

                "source": article.get(
                    "source",
                    {}
                ).get("name", "NewsAPI"),

                "url": article.get("url", ""),

                "published_at": article.get(
                    "publishedAt",
                    ""
                ),

                "clean_text": full_text,
            }
        )

    return articles