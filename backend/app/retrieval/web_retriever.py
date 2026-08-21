import re
from typing import List, Dict, Any
from app.ranking.model import ranking_model
import spacy

nlp = spacy.load("en_core_web_sm")

try:
    import wikipediaapi
except ImportError:
    wikipediaapi = None

from app.retrieval.evidence_schema import create_evidence


if wikipediaapi is not None:
    wiki = wikipediaapi.Wikipedia(
        language="en",
        user_agent="VeritasAI/1.0"
    )
else:
    wiki = None


def extract_entities(claim: str):

    doc = nlp(claim)

    entities = []
    seen = set()

    # -------------------------
    # Named Entities
    # -------------------------

    for ent in doc.ents:

        text = ent.text.strip()

        if (
            ent.label_ in {
                "PERSON",
                "ORG",
                "GPE",
                "LOC",
                "FAC",
                "PRODUCT",
                "EVENT",
                "WORK_OF_ART",
            }
            and len(text) > 2
            and text.lower() not in seen
        ):

            entities.append(text)
            seen.add(text.lower())

    # -------------------------
    # Important Noun Chunks
    # -------------------------

    STOP_CHUNKS = {
        "the",
        "a",
        "an",
        "this",
        "that",
        "these",
        "those",
        "it",
        "they",
        "he",
        "she",
        "we",
        "you",
        "i",
        "one",
        "something",
        "anything",
        "everything",
    }

    for chunk in doc.noun_chunks:

        text = chunk.text.strip()

        if text.lower().startswith("the "):
            text = text[4:]

        if (
            len(text) > 2
            and text.lower() not in STOP_CHUNKS
            and text.lower() not in seen
        ):

            entities.append(text)
            seen.add(text.lower())

    print("=" * 80)
    print("Extracted Entities:", entities)
    print("=" * 80)

    return entities

def wikipedia_search(claim: str) -> List[Dict[str, Any]]:

    if wiki is None:
        raise ImportError(
            "Install wikipedia-api using: pip install wikipedia-api"
        )

    entities = extract_entities(claim)

    print("=" * 80)
    print("Entities:", entities)
    print("=" * 80)

    all_results = []

    for entity in entities:

        print("Searching:", entity)

        page = wiki.page(entity)

        try:
            exists = page.exists()
        except Exception:
            exists = False

        print("Exists:", exists)

        if not exists:
            continue

        # -------------------------
        # Collect Wikipedia text
        # -------------------------

        text = page.summary

        for section in page.sections:

            if section.text.strip():

                text += "\n\n"

                text += section.text

        # -------------------------
        # Split into sentences
        # -------------------------

        sentences = re.split(
            r'(?<=[.!?])\s+',
            text
        )

        sentences = [
            s.strip()
            for s in sentences
            if s.strip()
        ]

        if not sentences:
            continue

        # -------------------------
        # Semantic ranking
        # -------------------------

        pairs = [
            (claim, sentence)
            for sentence in sentences
        ]

        scores = ranking_model.predict(pairs)

        ranked = sorted(
            zip(scores, sentences),
            key=lambda x: x[0],
            reverse=True
        )

        best_text = "\n".join(
            sentence
            for _, sentence in ranked[:10]
        )

        document = {
            "doc_id": page.title,
            "chunk_id": 0,
            "title": page.title,
            "source": "Wikipedia",
            "url": f"https://en.wikipedia.org/wiki/{page.title.replace(' ', '_')}",
            "published_at": None,
            "chunk_text": best_text,
        }

        all_results.append(
            create_evidence(
                document=document,
                retrieval_score=1.0,
                retriever="wikipedia",
            )
        )

    print("=" * 80)
    print("Wikipedia Results:", len(all_results))

    for item in all_results:
        print(item["document"]["title"])

    print("=" * 80)

    return all_results