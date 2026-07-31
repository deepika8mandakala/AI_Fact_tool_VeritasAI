from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAME = "typeform/distilbert-base-uncased-mnli"

_tokenizer = None
_model = None


def get_model():
    global _tokenizer, _model

    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    if _model is None:
        _model = AutoModelForSequenceClassification.from_pretrained(
            MODEL_NAME,
            low_cpu_mem_usage=True
        )
        print("Model labels:", _model.config.id2label)

    return _tokenizer, _model