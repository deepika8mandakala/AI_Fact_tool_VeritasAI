import re
from bs4 import BeautifulSoup


def clean_text(text: str) -> str:
    """
    Clean text for claim verification.
    """

    if not text:
        return ""

    # Remove HTML
    text = BeautifulSoup(
        text,
        "html.parser"
    ).get_text()

    # Remove URLs
    text = re.sub(
        r"http\S+|www\S+",
        "",
        text
    )

    # Remove @mentions
    text = re.sub(
        r"@\w+",
        "",
        text
    )

    # Remove hashtag symbol
    text = re.sub(
        r"#",
        "",
        text
    )

    # Remove emojis / non-ascii
    text = re.sub(
        r"[^\x00-\x7F]+",
        " ",
        text
    )

    # Normalize quotes
    text = (
        text.replace("“", '"')
            .replace("”", '"')
            .replace("’", "'")
            .replace("‘", "'")
    )

    # Remove repeated punctuation
    text = re.sub(
        r"[.]{2,}",
        ".",
        text
    )

    text = re.sub(
        r"[!]{2,}",
        "!",
        text
    )

    text = re.sub(
        r"[?]{2,}",
        "?",
        text
    )

    # Normalize spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()