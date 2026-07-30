import feedparser

RSS_FEEDS = {
    "Reuters": "https://feeds.reuters.com/reuters/topNews",
    "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
    "The Hindu": "https://www.thehindu.com/news/feeder/default.rss",
}


def fetch_rss():

    articles = []

    for source, url in RSS_FEEDS.items():

        feed = feedparser.parse(url)

        for entry in feed.entries:

            articles.append({

                "title": entry.get("title", ""),

                "source": source,

                "url": entry.get("link", ""),

                "published_at": entry.get("published", ""),

                "clean_text": entry.get("summary", "")
            })

    return articles