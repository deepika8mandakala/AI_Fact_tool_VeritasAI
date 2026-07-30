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

    scores = ranking_model.predict(pairs)

    ranked = []

    for item, score in zip(evidence, scores):

    # Cross-encoder score
        rerank_score = float(score)

    # Source credibility score
        source_score = get_source_score(
            item["document"].get("url", "")
        )

    # Retrieval score (already computed by FAISS)
        retrieval_score = item.get("retrieval_score", 0)

    # Final weighted score
        final_score = (
            0.40 * retrieval_score +
            0.40 * rerank_score +
            0.20 * source_score
        )

        item["rerank_score"] = rerank_score
        item["source_score"] = source_score
        item["final_score"] = final_score

        ranked.append(item)

    ranked.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return ranked