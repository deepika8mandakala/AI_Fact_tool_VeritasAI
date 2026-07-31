from transformers import pipeline

_classifier = None

MODEL_NAME = "typeform/distilbert-base-uncased-mnli"


def get_classifier():
    global _classifier

    if _classifier is None:
        _classifier = pipeline(
            "zero-shot-classification",
            model=MODEL_NAME
        )

    return _classifier