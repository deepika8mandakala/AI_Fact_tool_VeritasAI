from app.models.deberta import (
    get_model,
    get_tokenizer,
)


def get_verification_model():
    return (
        get_tokenizer(),
        get_model()
    )