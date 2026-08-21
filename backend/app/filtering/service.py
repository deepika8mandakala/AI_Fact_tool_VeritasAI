MIN_RERANK_SCORE = 0.25
MIN_RETRIEVAL_SCORE = 0.30


def filter_evidence(evidence):

    filtered = []

    for item in evidence:

        rerank_score = item.get(
            "rerank_score",
            0.0
        )

        retrieval_score = item.get(
            "retrieval_score",
            0.0
        )

        print(
            item["document"]["title"],
            "| Retrieval:",
            round(retrieval_score, 3),
            "| Rerank:",
            round(rerank_score, 3),
        )

        if (
            rerank_score >= MIN_RERANK_SCORE
            and retrieval_score >= MIN_RETRIEVAL_SCORE
        ):
            filtered.append(item)

    return filtered