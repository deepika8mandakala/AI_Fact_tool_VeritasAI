import re
from typing import Optional, List, Dict, Any

try:
    import wikipediaapi
except ImportError:  # pragma: no cover - informative fallback when package is missing
    wikipediaapi = None

from app.retrieval.evidence_schema import create_evidence

if wikipediaapi is not None:
    wiki = wikipediaapi.Wikipedia(
        language="en",
        user_agent="VeritasAI/1.0"
    )
else:
    wiki = None


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


def wikipedia_search(claim: str) -> List[Dict[str, Any]]:
    """Search Wikipedia for the main entity in a claim and return evidence-like results.

    Raises ImportError if the wikipediaapi package is not installed.
    """

    if wiki is None:
        raise ImportError(
            "wikipediaapi is not installed. Install it with: pip install wikipedia-api"
        )

    entity = extract_entity(claim)

    page = wiki.page(entity)

    if not page.exists():
        return []

    document = {
        "doc_id": page.fullurl,
        "chunk_id": 0,
        "title": page.title,
        "source": "Wikipedia",
        "url": page.fullurl,
        "published_at": None,
        "chunk_text": page.summary,
    }

    return [
        create_evidence(
            document=document,
            retrieval_score=1.0,
            retriever="wikipedia",
        )
    ]