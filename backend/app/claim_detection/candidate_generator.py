from app.entity_recognition.extractor import extract_entities

def is_claim_candidate(sentence):

    entities = extract_entities(sentence)

    if entities["numbers"]:
        return True

    if entities["persons"]:
        return True

    if entities["organizations"]:
        return True

    if entities["dates"]:
        return True

    return False