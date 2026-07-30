from collections import defaultdict


def aggregate_verdict(results):

    scores = defaultdict(float)

    for item in results:

        label = item["verdict"]

        confidence = item["confidence"]

        retrieval = item["retrieval_score"]

        rerank = item["rerank_score"]

        source = item["source_score"]

        final_score = (
            confidence * 0.50
            + retrieval * 0.15
            + rerank * 0.15
            + source * 0.20
        )

        scores[label] += final_score

    final_verdict = max(scores, key=scores.get)

    total = sum(scores.values())

    confidence = scores[final_verdict] / total if total else 0

    return {
        "final_verdict": final_verdict,
        "confidence": round(confidence, 3),
        "scores": dict(scores),
    }