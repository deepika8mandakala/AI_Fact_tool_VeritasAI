from collections import defaultdict


def aggregate_verdict(results):

    if not results:
        return {
            "final_verdict": "INSUFFICIENT_EVIDENCE",
            "confidence": 0.0,
            "scores": {},
            "conflict": False
        }

    scores = defaultdict(float)

    best_item = None
    best_score = -1

    for item in results:

        confidence = item.get("confidence", 0)
        relevance = item.get("relevance_score", 0)
        rerank = item.get("rerank_score", 0)
        retrieval = item.get("retrieval_score", 0)
        source = item.get("source_score", 0)

        overall_score = (
            0.40 * confidence +
            0.30 * rerank +
            0.20 * relevance +
            0.05 * retrieval +
            0.05 * source
        )

        scores[item["verdict"]] += overall_score

        if overall_score > best_score:
            best_score = overall_score
            best_item = item

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    conflict = False

    if len(ranked) > 1:

        if abs(ranked[0][1] - ranked[1][1]) < 0.25:
            conflict = True

    return {
        "final_verdict": best_item["verdict"],
        "confidence": round(best_item["confidence"], 3),
        "scores": dict(scores),
        "conflict": conflict
    }