from collections import Counter


def calculate_agreement(results):

    if not results:

        return {
            "agreement": 0.0,
            "majority": "INSUFFICIENT_EVIDENCE",
            "counts": {}
        }

    labels = [
        item["verdict"]
        for item in results
    ]

    counts = Counter(labels)

    majority = counts.most_common(1)[0][0]

    agreement = (
        counts[majority] /
        len(results)
    )

    return {
        "agreement": round(
            agreement * 100,
            2
        ),
        "majority": majority,
        "counts": dict(counts)
    }