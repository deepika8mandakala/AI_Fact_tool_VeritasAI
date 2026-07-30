import re
from bs4 import BeautifulSoup


def clean_text(text: str) -> str:
    """
    Clean raw text by removing HTML, URLs, mentions,
    hashtags, emojis, and extra spaces.
    """

    if not text:
        return ""

    # Remove HTML
    text = BeautifulSoup(text, "html.parser").get_text()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove @mentions
    text = re.sub(r"@\w+", "", text)

    # Remove hashtags (#keep the word)
    text = re.sub(r"#", "", text)

    # Remove non-ASCII characters (basic emoji cleanup)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()