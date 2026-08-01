import re
from typing import Optional, List, Dict, Any
import spacy

nlp = spacy.load("en_core_web_sm")
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


def extract_entity(claim: str):

    doc = nlp(claim)

    for token in doc:

        if token.dep_ == "nsubj":

            entity = " ".join(
                t.text
                for t in token.subtree
            )

            return entity

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