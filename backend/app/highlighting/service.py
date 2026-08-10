import re

from app.ranking.model import ranking_model


STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were",
    "to", "of", "in", "on", "for", "and", "with",
    "by", "at", "from", "that", "this"
}


IMPORTANT_TERMS = {
    "orbit": 2,
    "orbits": 2,
    "revolve": 2,
    "revolves": 2,
    "prime minister": 2,
    "president": 2,
    "capital": 2,
    "located": 2,
    "largest": 2,
    "smallest": 2,
}


def tokenize(text):

    return set(
        word
        for word in re.findall(
            r"[A-Za-z]+",
            text.lower()
        )
        if word not in STOPWORDS
    )


def extract_highlight(text: str, claim: str):

    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    if not sentences:
        return ""

    # ------------------------------------------------
    # Semantic ranking using existing CrossEncoder
    # ------------------------------------------------

    pairs = [
        (claim, sentence)
        for sentence in sentences
    ]

    semantic_scores = ranking_model.predict(pairs)

    claim_words = tokenize(claim)

    ranked = []

    for sentence, semantic_score in zip(
        sentences,
        semantic_scores
    ):

        words = tokenize(sentence)

        overlap = len(
            claim_words & words
        )

        keyword_bonus = 0

        lower = sentence.lower()

        for keyword, bonus in IMPORTANT_TERMS.items():

            if keyword in lower:
                keyword_bonus += bonus

        # Semantic relevance is the main signal.
        # Keyword overlap is only a small supporting signal.
        final_score = (
            float(semantic_score)
            + (overlap * 0.05)
            + (keyword_bonus * 0.02)
        )

        ranked.append(
            (
                final_score,
                sentence
            )
        )

    ranked.sort(
        key=lambda x: x[0],
        reverse=True
    )

    best_sentence = ranked[0][1]

    print("=" * 80)
    print("HIGHLIGHT")
    print("Claim:", claim)
    print("Selected:", best_sentence)
    print("=" * 80)

    return best_sentence