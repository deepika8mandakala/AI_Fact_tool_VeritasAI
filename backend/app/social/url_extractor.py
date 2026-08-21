import re


def extract_url(text: str):
    if not text:
        return None

    # Find the first HTTP/HTTPS URL.
    match = re.search(
        r"https?\s*:\s*/\s*/",
        text,
        flags=re.IGNORECASE,
    )

    if not match:
        return None

    candidate = text[match.start():]

    # Stop at common separators used by social/news posts.
    candidate = re.split(
        r"\s+(?:Paper|Summary|Source|Link)\s*:",
        candidate,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]

    # Stop at hashtags.
    candidate = re.split(
        r"\s+#",
        candidate,
        maxsplit=1,
    )[0]

    # Remove spaces inserted inside URLs.
    candidate = re.sub(
        r"\s+",
        "",
        candidate,
    )

    # Remove scheme spacing.
    candidate = re.sub(
        r"^https?\s*:\s*/\s*/",
        "",
        candidate,
        flags=re.IGNORECASE,
    )

    candidate = candidate.rstrip(
        ".,;!?)]}\"'📷:"
    )

    if not candidate:
        return None

    return "https://" + candidate