from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    pipeline,
)

MODEL_NAME = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"

_tokenizer = None
_model = None
_classifier = None


def get_tokenizer():
    global _tokenizer

    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    return _tokenizer


def get_model():
    global _model

    if _model is None:
        _model = AutoModelForSequenceClassification.from_pretrained(
            MODEL_NAME,
            low_cpu_mem_usage=True
        )

        print("Loaded shared DeBERTa model.")

    return _model


def get_classifier():
    global _classifier

    if _classifier is None:
        _classifier = pipeline(
            "zero-shot-classification",
            model=get_model(),
            tokenizer=get_tokenizer(),
            device=-1
        )

        print("Loaded shared Zero-Shot pipeline.")

    return _classifier