from typing import Dict

from app.claim_detection.model import get_classifier

LABELS = [
    "factual claim",
    "opinion",
    "question",
    "greeting",
    "prediction",
    "request",
]


def classify_claim(sentence: str) -> Dict:

    classifier = get_classifier()

    result = classifier(
        sentence,
        LABELS,
        multi_label=False,
    )

    top_label = result["labels"][0].lower()
    confidence = float(result["scores"][0])

    return {
        "is_claim": top_label == "factual claim",
        "label": top_label,
        "confidence": confidence,
    }