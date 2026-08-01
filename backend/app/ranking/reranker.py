from scipy.special import expit

from app.ranking.model import ranking_model
from app.ranking.source_ranker import get_source_score


def rerank(claim: str, evidence: list):

    if not evidence:
        return []

    pairs = [
        (
            claim,
            item["document"]["chunk_text"]
        )
        for item in evidence
    ]

    raw_scores = ranking_model.predict(pairs)

    ranked = []

    for item, raw_score in zip(evidence, raw_scores):

        retrieval_score = float(item.get("retrieval_score", 0.0))

        # Normalize retrieval score
        retrieval_score = max(0.0, min(1.0, retrieval_score))

        # Convert CrossEncoder logit → probability
        rerank_score = float(expit(raw_score))

        source_score = get_source_score(
            item["document"].get("url", "")
        )

        final_score = (
            0.40 * retrieval_score +
            0.40 * rerank_score +
            0.20 * source_score
        )

        item["retrieval_score"] = retrieval_score
        item["rerank_score"] = rerank_score
        item["source_score"] = source_score
        item["final_score"] = final_score

        ranked.append(item)

    ranked.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return ranked