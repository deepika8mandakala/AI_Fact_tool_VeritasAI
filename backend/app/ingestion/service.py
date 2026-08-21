from app.ingestion.newsapi import fetch_news
from app.ingestion.rss import fetch_rss


def collect_all_sources(query: str = "Artificial Intelligence"):

    articles = []

    articles.extend(fetch_news(query))
    articles.extend(fetch_rss())

    unique = {}

    for article in articles:
        url = article.get("url")

        if url:
            unique[url] = article

    return list(unique.values())