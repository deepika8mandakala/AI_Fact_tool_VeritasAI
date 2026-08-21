import feedparser


def latest_bbc_news():

    feed = feedparser.parse(
        "https://feeds.bbci.co.uk/news/rss.xml"
    )

    results = []

    for entry in feed.entries[:10]:

        results.append(
            {
                "title": entry.title,
                "url": entry.link,
                "summary": entry.summary,
            }
        )

    return results