import re
import wikipediaapi

wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent="VeritasAI/1.0"
)


def extract_entity(claim: str) -> str:
    """
    Extract the main entity from a factual claim.
    """

    claim = claim.strip()

    patterns = [
        r"^(.*?)\s+is\s+",
        r"^(.*?)\s+was\s+",
        r"^(.*?)\s+are\s+",
        r"^(.*?)\s+were\s+",
        r"^(.*?)\s+has\s+",
        r"^(.*?)\s+have\s+",
        r"^(.*?)\s+can\s+",
        r"^(.*?)\s+will\s+",
        r"^(.*?)\s+contains\s+",
    ]

    for pattern in patterns:

        match = re.match(pattern, claim, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return claim


def wikipedia_search(claim: str):

    entity = extract_entity(claim)

    page = wiki.page(entity)

    if not page.exists():
        return []

    return [
    {
        "document": {
            "doc_id": page.fullurl,
            "chunk_id": 0,
            "title": page.title,
            "source": "Wikipedia",
            "url": page.fullurl,
            "published_at": None,
            "chunk_text": page.summary,
        },
        "retrieval_score": 1.0
    }
]