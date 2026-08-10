from bs4 import BeautifulSoup


def extract_post(post):

    account = post.get("account", {})
    content = post.get("content", "")

    text = BeautifulSoup(
        content,
        "html.parser"
    ).get_text(
        " ",
        strip=True
    )

    # Mastodon link preview
    card = post.get("card") or {}

    card_title = card.get(
        "title",
        ""
    ).strip()

    card_description = card.get(
        "description",
        ""
    ).strip()

    # Add useful factual information from
    # the linked article preview.
    if card_description and card_description not in text:
        text = f"{text}.{card_description}".strip()

    return {
        "id": post.get("id"),
        "text": text,
        "url": post.get("url"),
        "created_at": post.get("created_at"),
        "visibility": post.get("visibility"),

        "article_url": card.get(
            "url"
        ),

        "article_title": card_title,

        "article_description": card_description,

        "account": {
            "username": account.get(
                "username"
            ),
            "acct": account.get(
                "acct"
            ),
            "display_name": account.get(
                "display_name"
            ),
        },

        "media": post.get(
            "media_attachments",
            []
        ),
    }