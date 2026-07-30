NEWS_KEYWORDS = [
    "today",
    "yesterday",
    "breaking",
    "announced",
    "reported"
]

MEDICAL_KEYWORDS = [
    "covid",
    "virus",
    "disease",
    "vaccine",
    "hospital"
]

STATISTICAL_KEYWORDS = [
    "population",
    "gdp",
    "inflation",
    "percentage"
]

SCIENTIFIC_KEYWORDS = [
    "gravity",
    "planet",
    "atom",
    "biology",
    "physics"
]


def classify_claim(claim: str):

    claim = claim.lower()

    if any(word in claim for word in MEDICAL_KEYWORDS):
        return "medical"

    if any(word in claim for word in NEWS_KEYWORDS):
        return "news"

    if any(word in claim for word in STATISTICAL_KEYWORDS):
        return "statistical"

    if any(word in claim for word in SCIENTIFIC_KEYWORDS):
        return "scientific"

    return "entity"