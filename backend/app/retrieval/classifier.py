import re


NEWS_DOMAINS = {
    "bbc.com",
    "bbc.co.uk",
    "reuters.com",
    "apnews.com",
    "theguardian.com",
    "sciencedaily.com",
    "sciencealert.com",
    "scitechdaily.com",
    "phys.org",
    "livescience.com",
    "nature.com",
    "nasa.gov",
    "space.com",
    "cbc.ca",
}


NEWS_KEYWORDS = {
    "today",
    "yesterday",
    "breaking",
    "latest",
    "recent",
    "announced",
    "announcement",
    "news",
    "reported",
    "report",
    "study",
    "research",
    "scientists",
    "researchers",
    "2025",
    "2026",
    "election",
    "earthquake",
    "flood",
    "war",
}


def is_news_claim(text: str) -> bool:

    if not text:
        return False

    text_lower = text.lower()

    # Current/news article URL.
    for domain in NEWS_DOMAINS:

        if domain in text_lower:
            return True

    # News/current-event language.
    for keyword in NEWS_KEYWORDS:

        if re.search(
            rf"\b{re.escape(keyword)}\b",
            text_lower
        ):
            return True

    return False