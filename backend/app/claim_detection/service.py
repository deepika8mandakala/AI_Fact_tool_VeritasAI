from app.claim_detection.extractor import split_into_sentences
from app.claim_detection.classifier import classify_claim
from app.entity_recognition.extractor import extract_entities


def detect_claims(text: str):

    sentences = split_into_sentences(text)

    claims = []

    for sentence in sentences:

        prediction = classify_claim(sentence)

        if prediction["is_claim"]:

            entities = extract_entities(sentence)

            claims.append(
                {
                    "claim": sentence,
                    "entities": entities,
                    "confidence": prediction["confidence"]
                }
            )

    return {
        "claims": claims,
        "total_claims": len(claims)
    }