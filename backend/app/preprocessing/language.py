from langdetect import detect


def detect_language(text: str):

    try:
        return detect(text)

    except Exception:
        return "unknown"