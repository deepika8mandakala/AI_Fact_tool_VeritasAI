from app.claim_detection.extractor import split_into_sentences
from app.entity_recognition.extractor import extract_entities


def detect_claims(text: str):

    sentences = split_into_sentences(text)

    claims = []

    for sentence in sentences:

        sentence = sentence.strip()

        # Skip very short sentences
        if len(sentence.split()) < 8:
            continue

        # Skip questions
        if sentence.endswith("?"):
            continue

        # Skip common non-content lines
        lower = sentence.lower()

        if lower.startswith("advertisement"):
            continue

        if lower.startswith("read more"):
            continue

        if lower.startswith("share"):
            continue

        if lower.startswith("follow us"):
            continue

        entities = extract_entities(sentence)

        claims.append(
            {
                "claim": sentence,
                "entities": entities,
                "confidence": 1.0
            }
        )

    return {
        "claims": claims,
        "total_claims": len(claims)
    }