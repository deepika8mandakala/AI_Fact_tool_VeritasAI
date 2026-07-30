MIN_RERANK_SCORE = 1.0
MIN_RETRIEVAL_SCORE = 0.70


def filter_evidence(evidence):

    filtered = []

    for item in evidence:

        rerank_score = item.get("rerank_score", 0.0)
        retrieval_score = item.get("retrieval_score", 0.0)

        if (
            rerank_score >= MIN_RERANK_SCORE
            and retrieval_score >= MIN_RETRIEVAL_SCORE
        ):
            filtered.append(item)

    if not filtered:

        filtered = sorted(
            evidence,
            key=lambda x: x.get("rerank_score", 0),
            reverse=True
        )[:3]

    return filtered