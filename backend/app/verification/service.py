from app.verification.verifier import verify_claim
from app.highlighting.service import extract_highlight


def verify_evidence(claim: str, evidence_list: list):

    results = []

    for item in evidence_list:

        print("\nVERIFICATION INPUT")
        print(item.keys())

        verdict = verify_claim(
            claim,
            item["document"]["chunk_text"]
        )

        results.append(
            {
                "document": item["document"],

                "retrieval_score": item.get(
                    "retrieval_score",
                    0.0
                ),

                "rerank_score": item.get(
                    "rerank_score",
                    0.0
                ),

                "source_score": item.get(
                    "source_score",
                    0.60
                ),
                "freshness_score": item.get(
                    "freshness_score",
                    0.50
                ),
                "quality_score": item.get(
                    "quality_score",
                    0
                ),

                "quality_label": item.get(
                    "quality_label",
                    "Unknown"
                ),

                "stars": item.get(
                    "stars",
                    0
                ),
                "bias": item.get(
                    "bias",
                    "Unknown"
                ),

                "reliability": item.get(
                    "reliability",
                    "Unknown"
                ),

                "category": item.get(
                    "category",
                    "Unknown"
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