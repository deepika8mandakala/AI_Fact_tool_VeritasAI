import hashlib


def generate_hash(text: str):
    return hashlib.md5(
        text.encode("utf-8")
    ).hexdigest()


def remove_duplicates(documents):

    seen = set()

    unique_docs = []

    for doc in documents:

        hash_value = generate_hash(
            doc["clean_text"]
        )

        if hash_value not in seen:

            seen.add(hash_value)

            unique_docs.append(doc)

    return unique_docs