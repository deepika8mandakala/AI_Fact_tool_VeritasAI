from sentence_transformers import CrossEncoder

model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def filter_relevant_evidence(
    claim: str,
    evidence: list,
    threshold: float = 0.15
):

    if not evidence:
        return []

    pairs = [
        (
            claim,
            item["document"]["chunk_text"]
        )
        for item in evidence
    ]

    scores = model.predict(pairs)

    print("=" * 80)
    print("RELEVANCE SCORES")

    for item, score in zip(evidence, scores):
        print(
            item["document"]["title"],
            "->",
            float(score)
        )

    print("=" * 80)

    filtered = []

    for item, score in zip(evidence, scores):

        item["relevance_score"] = float(score)

        print(
            item["document"]["title"],
            "->",
            round(float(score), 3)
        )

        if score >= threshold:

            filtered.append(item)

    # If nothing passes, keep the best 3
    if not filtered:

        evidence = sorted(
            evidence,
            key=lambda x: x["relevance_score"],
            reverse=True
        )

        filtered = evidence[:3]

        print("Keeping Top-3 evidence.")

    return filtered