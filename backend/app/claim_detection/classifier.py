from typing import Dict

from app.claim_detection.model import classifier

# Labels for NLI-based claim detection
LABELS = [
    "factual claim",
    "opinion",
    "question",
    "greeting",
    "prediction",
    "request"
]


def classify_claim(sentence: str) -> Dict:
    """
    Classify whether a sentence is a factual claim.

    Returns:
    {
        "is_claim": True,
        "label": "factual claim",
        "confidence": 0.93
    }
    """

    result = classifier(
        sentence,
        LABELS,
        multi_label=False
    )

    top_label = result["labels"][0].lower()
    confidence = round(float(result["scores"][0]), 4)

    return {
        "is_claim": top_label == "factual claim",
        "label": top_label,
        "confidence": confidence
    }