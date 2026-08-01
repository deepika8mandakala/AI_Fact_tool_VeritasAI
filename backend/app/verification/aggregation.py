from collections import defaultdict

from collections import defaultdict
import math


def aggregate_verdict(results):

    scores = defaultdict(float)

    for item in results:

        label = item["verdict"]

        confidence = item["confidence"]

        retrieval = item["retrieval_score"]

        rerank = item["rerank_score"]

        source = item["source_score"]

        final_score = (
            confidence * 0.50 +
            retrieval * 0.15 +
            rerank * 0.15 +
            source * 0.20
        )

        scores[label] += final_score

    if not scores:

        return {
            "final_verdict": "INSUFFICIENT_EVIDENCE",
            "confidence": 0.0,
            "scores": {},
            "conflict": False
        }

    # -----------------------------
    # Sort verdicts by score
    # -----------------------------

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    final_verdict = ranked[0][0]

    total = sum(scores.values())

    confidence = (
        ranked[0][1] / total
        if total else 0
    )

    # -----------------------------
    # Conflict Detection
    # -----------------------------

    conflict = False

    if len(ranked) > 1:

        difference = ranked[0][1] - ranked[1][1]

        # Less than 10% difference
        if difference < 0.10:

            conflict = True

    return {

        "final_verdict": final_verdict,

        "confidence": round(confidence, 3),

        "scores": dict(scores),

        "conflict": conflict
    }