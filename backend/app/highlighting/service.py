import re

STOPWORDS = {
    "the","a","an","is","are","was","were",
    "to","of","in","on","for","and","with",
    "by","at","from","that","this"
}


IMPORTANT_TERMS = {
    "orbit":6,
    "orbits":6,
    "revolve":6,
    "revolves":6,
    "prime minister":6,
    "president":6,
    "capital":5,
    "located":3,
    "largest":3,
    "smallest":3
}


def tokenize(text):

    return set(
        w
        for w in re.findall(r"[A-Za-z]+", text.lower())
        if w not in STOPWORDS
    )


def extract_highlight(text, claim):

    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    claim_words = tokenize(claim)

    best_sentence = ""
    best_score = -1

    for sentence in sentences:

        words = tokenize(sentence)

        overlap = len(
            claim_words & words
        )

        score = overlap * 2

        lower = sentence.lower()

        for keyword, bonus in IMPORTANT_TERMS.items():

            if keyword in lower:
                score += bonus

        if len(sentence) < 30:
            score -= 2

        if score > best_score:
            best_score = score
            best_sentence = sentence

    return best_sentence.strip()