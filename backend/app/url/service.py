from newspaper import Article


def extract_article(url: str):

    print("=" * 80)
    print("URL RECEIVED:", repr(url))
    print("=" * 80)

    article = Article(url)

    article.download()
    article.parse()

    return {
        "title": article.title,
        "text": article.text,
        "authors": article.authors,
        "publish_date": article.publish_date,
    }