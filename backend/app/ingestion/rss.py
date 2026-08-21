import feedparser
from newspaper import Article

RSS_FEEDS = {
    "Reuters": "https://feeds.reuters.com/reuters/topNews",
    "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
    "The Hindu": "https://www.thehindu.com/news/feeder/default.rss",
}


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


def fetch_rss():

    articles = []

    for source, url in RSS_FEEDS.items():

        print(f"Fetching {source}...")

        feed = feedparser.parse(url)

        for entry in feed.entries:

            full_text = fetch_article(
                entry.get("link", "")
            )

            # fallback if article download fails
            if not full_text:
                full_text = entry.get("summary", "")

            articles.append({

                "title": entry.get("title", ""),

                "source": source,

                "url": entry.get("link", ""),

                "published_at": entry.get("published", ""),

                "clean_text": full_text

            })

    return articles