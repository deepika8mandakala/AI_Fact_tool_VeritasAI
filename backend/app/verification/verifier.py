import torch
from torch.nn.functional import softmax

from app.verification.model import tokenizer, model

LABEL_MAP = {
    "ENTAILMENT": "SUPPORTED",
    "CONTRADICTION": "CONTRADICTED",
    "NEUTRAL": "INSUFFICIENT_EVIDENCE"
}


def verify_claim(claim: str, evidence: str):
    """
    Verify a claim against one evidence chunk.
    """

    inputs = tokenizer(
        claim,
        evidence,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = softmax(outputs.logits, dim=1)[0]

    best_index = torch.argmax(probabilities).item()

    label = model.config.id2label[best_index]

    return {
        "label": LABEL_MAP[label.upper()],
        "confidence": float(probabilities[best_index])
    }