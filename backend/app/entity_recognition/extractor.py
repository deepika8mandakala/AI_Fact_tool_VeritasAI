from app.entity_recognition.model import nlp
from app.entity_recognition.normalizer import normalize_entity

def extract_entities(text: str):

    doc = nlp(text)

    entities = {
        "persons": [],
        "organizations": [],
        "locations": [],
        "dates": [],
        "numbers": []
    }

    for ent in doc.ents:

        if ent.label_ == "PERSON":
            entities["persons"].append(
                normalize_entity(ent.text)
            )

        elif ent.label_ == "ORG":
            entities["organizations"].append(ent.text)

        elif ent.label_ in ["GPE", "LOC"]:
            entities["locations"].append(ent.text)

        elif ent.label_ == "DATE":
            entities["dates"].append(ent.text)

        elif ent.label_ in ["PERCENT", "MONEY", "CARDINAL", "QUANTITY"]:
            entities["numbers"].append(ent.text)

    # Remove duplicates
    for key in entities:
        entities[key] = list(set(entities[key]))

    return entities