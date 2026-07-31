from app.preprocessing.clean import clean_text
from app.preprocessing.language import detect_language
from app.preprocessing.translator import translate_to_english
from app.preprocessing.duplicates import remove_duplicates


def preprocess_document(document):

    # Accept both raw string and document dictionary
    if isinstance(document, str):
        raw_text = document

        cleaned = clean_text(raw_text)

        language = detect_language(cleaned)

        translated = translate_to_english(
            cleaned,
            language
        )

        return {
            "clean_text": translated,
            "language": language
        }

    # Dictionary input (news articles)
    raw_text = document.get("clean_text", "")

    cleaned = clean_text(raw_text)

    language = detect_language(cleaned)

    translated = translate_to_english(
        cleaned,
        language
    )

    return {
        "title": document.get("title", ""),
        "source": document.get("source", ""),
        "url": document.get("url", ""),
        "published_at": document.get("published_at", ""),
        "clean_text": translated,
        "language": language
    }


def preprocess_documents(documents):

    processed = []

    for doc in documents:
        processed.append(
            preprocess_document(doc)
        )

    return remove_duplicates(processed)