from app.credibility.source_scores import SOURCE_CREDIBILITY


DEFAULT_SCORE = 0.70


def get_source_score(source: str):

    if not source:
        return DEFAULT_SCORE

    for key, value in SOURCE_CREDIBILITY.items():

        if key.lower() in source.lower():
            return value

    return DEFAULT_SCORE