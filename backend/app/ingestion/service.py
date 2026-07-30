from app.ingestion.newsapi import fetch_news
from app.ingestion.rss import fetch_rss


def collect_all_sources(query: str = "Artificial Intelligence"):

    articles = []

    articles.extend(fetch_news(query))

    articles.extend(fetch_rss())

    return articles