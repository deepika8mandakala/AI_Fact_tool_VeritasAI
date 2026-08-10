import re

import torch
from torch.nn.functional import softmax

from app.verification.model import get_verification_model


LABEL_MAP = {
    "entailment": "SUPPORTED",
    "neutral": "INSUFFICIENT_EVIDENCE",
    "contradiction": "CONTRADICTED",
}


def normalize(text: str) -> str:
    """
    Normalize text for simple rule matching.
    """

    if not text:
        return ""

    text = text.lower()

    text = re.sub(
        r"[^\w\s]",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def verify_claim(
    claim: str,
    evidence: str,
):
    """
    Verify a claim against supplied evidence
    using the DeBERTa NLI model.
    """

    tokenizer, model = get_verification_model()

    # --------------------------------------------------
    # Debug information
    # --------------------------------------------------

    print("=" * 80)
    print("CLAIM:")
    print(claim)

    print("\nEVIDENCE:")
    print(evidence)

    print("=" * 80)

    claim_norm = normalize(claim)
    evidence_norm = normalize(evidence)

    print("NORMALIZED CLAIM:")
    print(claim_norm)

    print("\nNORMALIZED EVIDENCE:")
    print(evidence_norm)

    print("=" * 80)

    # --------------------------------------------------
    # NLI Verification
    # --------------------------------------------------

    inputs = tokenizer(
        evidence,
        claim,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512,
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = softmax(
        outputs.logits,
        dim=1,
    )[0]

    print(
        "id2label:",
        model.config.id2label,
    )

    print(
        "probabilities:",
        probabilities.tolist(),
    )

    best_index = torch.argmax(
        probabilities
    ).item()

    raw_label = model.config.id2label[
        best_index
    ]

    confidence = float(
        probabilities[best_index]
    )

    label = LABEL_MAP.get(
        raw_label.lower(),
        "INSUFFICIENT_EVIDENCE",
    )
    # Low confidence → insufficient evidence
    if confidence < 0.60:
        label = "INSUFFICIENT_EVIDENCE"

    print(
        "FINAL LABEL:",
        label,
    )

    print(
        "CONFIDENCE:",
        confidence,
    )

    return {
        "label": label,
        "confidence": confidence,
    }


def _first_color(
    text: str,
    colors: list[str],
) -> str | None:
    """
    Find the first explicitly mentioned color.
    Uses word boundaries to avoid matching words
    such as 'red' inside 'hundred'.
    """

    text_norm = normalize(text)

    for color in colors:

        if re.search(
            rf"\b{re.escape(color)}\b",
            text_norm,
        ):
            return color

    return None


def _collect_color_sentences(
    evidence: str,
    colors: list[str],
) -> list[str]:
    """
    Collect evidence sentences containing
    an explicitly mentioned color.
    """

    color_sentences = []

    sentences = re.split(
        r"(?<=[.!?])\s+",
        evidence,
    )

    for sentence in sentences:

        sentence_norm = normalize(
            sentence
        )

        if any(
            re.search(
                rf"\b{re.escape(color)}\b",
                sentence_norm,
            )
            for color in colors
        ):
            color_sentences.append(
                sentence_norm
            )

    return color_sentences


def _has_contradictory_color(
    sentence: str,
    claim_color: str,
    colors: list[str],
) -> bool:
    """
    Check whether a sentence explicitly contains
    a different color.

    Kept as a helper for compatibility with the
    existing project structure.
    """

    for color in colors:

        if color == claim_color:
            continue

        if re.search(
            rf"\b{re.escape(color)}\b",
            sentence,
        ):
            return True

    return False


def check_color_contradiction():
    return None