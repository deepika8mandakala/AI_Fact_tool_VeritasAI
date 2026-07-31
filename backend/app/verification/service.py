from app.verification.verifier import verify_claim
from app.credibility.service import get_source_score
from app.highlighting.service import extract_highlight


def verify_evidence(claim: str, evidence_list: list):

    results = []

    for item in evidence_list:

        verdict = verify_claim(
            claim,
            item["document"]["chunk_text"]
        )

        results.append(
        {
            "document": item["document"],

            "retrieval_score": item.get("retrieval_score", 0.0),

            "rerank_score": item.get(
                "rerank_score",
                item.get("retrieval_score", 0.0),
            ),

            "source_score": get_source_score(
                item["document"]["source"]
            ),

            "highlight": extract_highlight(
                item["document"]["chunk_text"],
                claim
            ),

            "verdict": verdict["label"],

            "confidence": verdict["confidence"]
        }
    )

    return results