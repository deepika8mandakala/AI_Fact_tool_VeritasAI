from typing import Dict
import re

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

    sentence = sentence.strip()

    if len(sentence) < 10:
        return {
            "is_claim": False,
            "label": "too_short",
            "confidence": 1.0,
        }

    # Questions
    if sentence.endswith("?"):
        return {
            "is_claim": False,
            "label": "question",
            "confidence": 1.0,
        }

    # Greetings
    if re.match(
        r"^(hi|hello|hey|good morning|good evening|thanks|thank you)\b",
        sentence.lower()
    ):
        return {
            "is_claim": False,
            "label": "greeting",
            "confidence": 1.0,
        }

    classifier = get_classifier()

    result = classifier(
        sentence,
        LABELS,
        multi_label=False,
    )

    top_label = result["labels"][0].lower()
    confidence = float(result["scores"][0])

    # Require reasonable confidence
    is_claim = (
        top_label == "factual claim"
        and confidence >= 0.60
    )

    return {
        "is_claim": is_claim,
        "label": top_label,
        "confidence": confidence,
    }