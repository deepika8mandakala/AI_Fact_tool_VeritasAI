import re


def extract_highlight(text: str, claim: str):

    sentences = re.split(r'(?<=[.!?])\s+', text)

    claim_words = set(
        claim.lower().split()
    )

    best_sentence = ""
    best_score = -1

    for sentence in sentences:

        words = set(sentence.lower().split())

        score = len(
            claim_words.intersection(words)
        )

        if score > best_score:

            best_score = score

            best_sentence = sentence

    return best_sentence