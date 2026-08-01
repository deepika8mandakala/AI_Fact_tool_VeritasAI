NEWS_KEYWORDS = [

    "today",

    "yesterday",

    "week",

    "month",

    "breaking",

    "announced",

    "said",

    "meeting",

    "election",

    "war",

    "flood",

    "earthquake"
]


def is_news_claim(claim):

    claim = claim.lower()

    return any(

        word in claim

        for word in NEWS_KEYWORDS

    )