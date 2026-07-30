ENTITY_ALIASES = {
    "PM Modi": "Narendra Modi",
    "Modi": "Narendra Modi",
    "WHO": "World Health Organization",
    "US": "United States"
}

def normalize_entity(entity: str):
    return ENTITY_ALIASES.get(entity, entity)