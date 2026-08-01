import torch
from torch.nn.functional import softmax
from app.verification.model import get_verification_model

LABEL_MAP = {
    "entailment": "SUPPORTED",
    "neutral": "INSUFFICIENT_EVIDENCE",
    "contradiction": "CONTRADICTED",

    "ENTAILMENT": "SUPPORTED",
    "NEUTRAL": "INSUFFICIENT_EVIDENCE",
    "CONTRADICTION": "CONTRADICTED",
}


def verify_claim(claim: str, evidence: str):

    tokenizer, model = get_verification_model()

    inputs = tokenizer(
        evidence,
        claim,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = softmax(outputs.logits, dim=1)[0]

    print("id2label:", model.config.id2label)
    print("probabilities:", probabilities.tolist())

    best_index = torch.argmax(probabilities).item()

    raw_label = model.config.id2label[best_index]
    return {
        "label": LABEL_MAP.get(raw_label.lower(), raw_label),
        "confidence": float(probabilities[best_index])
    }