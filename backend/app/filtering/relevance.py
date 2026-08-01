from sentence_transformers import CrossEncoder

model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def filter_relevant_evidence(
    claim: str,
    evidence: list,
    threshold: float = 0.35
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

    filtered = []

    for item, score in zip(evidence, scores):

        item["relevance_score"] = float(score)

        if score >= threshold:

            filtered.append(item)

    return filtered