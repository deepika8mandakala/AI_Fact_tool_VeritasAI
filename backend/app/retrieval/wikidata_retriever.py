import requests
from app.retrieval.evidence_schema import create_evidence

SEARCH_URL = "https://www.wikidata.org/w/api.php"


def wikidata_search(claim: str):

    params = {
        "action": "wbsearchentities",
        "search": claim,
        "language": "en",
        "format": "json"
    }

    try:
        headers = {
            "User-Agent": "VeritasAI/1.0 (research project)"
        }

        response = requests.get(
            SEARCH_URL,
            params=params,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

    except Exception as e:
        print("Wikidata Error:", e)
        return []

    evidence = []

    for item in data.get("search", [])[:3]:

        document = {
            "doc_id": item.get("id"),
            "chunk_id": 0,
            "title": item.get("label"),
            "source": "Wikidata",
            "url": f"https://www.wikidata.org/wiki/{item.get('id')}",
            "published_at": None,
            "chunk_text": item.get("description", ""),
        }

        evidence.append(
            create_evidence(
                document=document,
                retrieval_score=0.95,
                retriever="wikidata",
            )
        )

    return evidence