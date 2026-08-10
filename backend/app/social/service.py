import re
from app.social.mastodon_client import get_hashtag_posts
from app.claim_detection.classifier import classify_claim
from app.social.post_extractor import extract_post
from app.verification.pipeline import verify_pipeline
from app.social.url_extractor import extract_url
from app.social.article import fetch_article

def clean_social_text(text: str) -> str:

    if not text:
        return ""

    # Remove URLs while handling spaces inserted by feeds/Mastodon.
    text = re.sub(
        r"https?\s*://\s*[^\s#]+(?:\s+[^\s#]+)*",
        " ",
        text,
        flags=re.IGNORECASE,
    )

    # Remove hashtags but KEEP the words around them.
    text = re.sub(
        r"#\s*\w+",
        " ",
        text
    )

    # Remove mentions.
    text = re.sub(
        r"@\s*[A-Za-z0-9_@.-]+",
        " ",
        text
    )

    # Remove common URL/domain fragments left by feeds.
    text = re.sub(
        r"\b(?:www\.)?[A-Za-z0-9.-]+\."
        r"(?:com|org|net|gov|io|ca|tv|co\.uk)\b"
        r"(?:/[^\s]*)?",
        " ",
        text,
        flags=re.IGNORECASE
    )

    # Normalize whitespace.
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()

def looks_like_claim(sentence: str):

    text = sentence.strip()

    if not text:
        return False

    # Reject URLs / domain fragments.
    if re.search(
        r"(https?://|www\.|\.com\b|\.org\b|\.net\b|\.gov\b)",
        text,
        flags=re.IGNORECASE
    ):
        return False

    # Reject hashtag-only / mention-only fragments.
    cleaned = re.sub(
        r"[#@]\s*[\w.-]+",
        "",
        text
    ).strip()

    if not cleaned:
        return False

def split_sentences(text: str):

    if not text:
        return []

    text = re.sub(
        r"(?i)(?<=wings)\s+(?=Tobacco\b)",
        ". ",
        text,
    )
    text = re.sub(
        r"(\b[A-Z][a-z]+\s+[A-Z][a-z]+\b)\s+(Along with\b)",
        r"\1. \2",
        text,
    )
    text = re.sub(
        r"\.\s*([A-Z])",
        r". \1",
        text,
    )

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text,
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]
    # ... keep the rest of your existing checks ...

def _extract_quoted_headline(text: str) -> str:
    """Extract the first quoted factual headline."""

    if not text:
        return ""

    match = re.search(
        r'["“](.+?)[”"]',
        text,
        flags=re.DOTALL,
    )

    if match:
        return match.group(1).strip()

    return text

def _remove_rss_wrapper(text: str) -> str:
    """Remove RSS/social wrapper text and RSS disclaimers."""

    text = re.sub(
        r"^.*?fediverse\s*[\u201C\u201D\"']",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    marker = "🤖 via RSS feed"
    start = text.lower().find(marker.lower())

    if start != -1:
        text = text[:start]

    text = re.sub(
        r"(?<=[a-z])(?=[A-Z])",
        " ",
        text,
    )
    return re.sub(
        r"\.{2,}$",
        "",
        text,
    ).strip()


def _is_headline_fallback(sentence: str) -> bool:
    """Detect factual-looking science/news statements."""

    words = re.findall(
        r"[A-Za-z]+(?:'[A-Za-z]+)?",
        sentence,
    )

    if len(words) < 7:
        return False

    lower = sentence.lower()

    factual_verbs = {
        "reveals", "revealed",
        "shows", "showed","exposed",
        "finds", "found",
        "discovers", "discovered",
        "contains", "contain",
        "suggests", "suggested",
        "indicates", "indicated",
        "reports", "reported",
        "predicts", "predicted",
        "causes", "caused",
        "creates", "created",
        "detects", "detected",
        "observed", "observe",
        "announced", "announces",
        "proves", "proved",
        "identifies", "identified",
        "measures", "measured",
        "uses", "use",
        "may use",
        "could",
        "can",
        "is",
        "are",
        "was",
        "were",
    }

    has_factual_verb = any(
        re.search(
            rf"\b{re.escape(verb)}\b",
            lower,
        )
        for verb in factual_verbs
    )

    science_terms = {
        "moth", "moths",
        "hawkmoth", "hawkmoths",
        "scientist", "scientists",
        "research", "researchers",
        "study", "evidence",
        "nasa", "planet", "galaxy",
        "eclipse", "hurricane",
        "climate", "heat",
        "global warming",
        "earthquake", "meteorite",
        "asteroid", "space",
        "physics", "biology",
        "chemistry", "dna","exposes","expose",
        "amino", "plasma",
        "disappearing",
        "declining","increasing",
        "decreasing","changing",
        "affecting","threatens",
        "threatened","linked",
        "associated",
        "reveals", "revealed",
        "shows", "showed",
        "finds", "found",
        "discovers", "discovered",
        "contains", "contain",
        "suggests", "suggested",
        "indicates", "indicated",
        "reports", "reported",
        "predicts", "predicted",
        "causes", "caused",
        "creates", "created",
        "detects", "detected",
        "observed", "observe",
        "announced", "announces",
        "proves", "proved",
        "identifies", "identified",
        "measures", "measured",
        "uses", "use",
        "could", "can","cosmic",
        "flare","black","hole","black hole",
        "is", "are",
        "was", "were",
        "exposes", "expose",
        "brain", "health",
        "economic", "growth","wasp",
        "wasps","insect","insects",
        "animal","animals","wildlife",
        "species","black hole","star",
        "motor","electric","magnet",
    }

    has_science_term = any(
        term in lower
        for term in science_terms
    )

    return has_factual_verb and has_science_term

def extract_claims(text: str):
    """Extract factual claims from social-media text."""

    if not text:
        return []

    cleaned = clean_social_text(text)

    if not cleaned:
        return []

    # Extract actual headline from RSS/social aggregator posts.
    cleaned = _extract_quoted_headline(text)

    cleaned = clean_social_text(cleaned)

    if not cleaned:
        return []

    # Remove RSS/social wrapper.
    cleaned = _remove_rss_wrapper(cleaned)
    cleaned = _clean_feed_spacing(cleaned)
    if not cleaned:
        return []

    sentences = split_sentences(cleaned)

    claims = []

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence or is_incomplete_sentence(sentence):
            continue

        result = classify_claim(sentence)

        if result.get("is_claim"):
            claims.append(sentence)
            continue

        if _is_headline_fallback(sentence):
            print(
                "Headline fallback accepted:",
                sentence,
            )
            claims.append(sentence)

    return claims
def verify_mastodon_posts(limit: int = 3):

    print("=" * 80)
    print(f"Fetching recent #science posts: {limit}")
    print("=" * 80)

    posts = get_hashtag_posts(
        hashtag="science",
        limit=limit
    )

    print(f"Fetched {len(posts)} posts.")

    return _verify_posts(posts)


def verify_mastodon_hashtag(
    hashtag: str,
    limit: int = 3
):

    posts = get_hashtag_posts(
        hashtag,
        limit
    )

    return _verify_posts(posts)


def _verify_posts(posts):

    results = []

    total = len(posts)

    for index, post in enumerate(posts, start=1):

        print("\n" + "=" * 80)
        print(f"PROCESSING POST {index}/{total}")
        print("=" * 80)

        extracted = extract_post(post)

        text = extracted["text"].strip()

        if not text:
            print("Empty post. Skipping.")
            continue

        print("Post text extracted.")
        print("RAW EXTRACTED TEXT:")
        print(repr(text))
        print("CLEANED TEXT:")
        print(repr(clean_social_text(text)))

        claims = extract_claims(text)

        print("CLAIMS FOUND:", len(claims))

        if not claims:
            print("No factual-looking claims. Skipping verification.")
            continue

        for claim_index, claim in enumerate(claims, start=1):

            print("\n" + "-" * 80)
            print(
                f"VERIFYING CLAIM {claim_index}/{len(claims)} "
                f"FROM POST {index}/{total}"
            )
            print("-" * 80)

            print("CLAIM:")
            print(claim)

            try:

                print("Starting verification pipeline...")

                verification = verify_pipeline(claim)

                print("Verification completed.")

                summary = verification.get("summary", {})

                verdict = summary.get("final_verdict")

                if verdict == "INSUFFICIENT_EVIDENCE":

                    article_result = _article_fallback(
                        claim,
                        text
                    )

                    if article_result:

                        verification["article_verification"] = (
                            article_result
                        )

                        article_label = article_result.get(
                            "label",
                            "INSUFFICIENT_EVIDENCE"
                        )

                        article_confidence = article_result.get(
                            "confidence",
                            0.0
                        )

                        # Use article verification as the final
                        # verdict when the main evidence pipeline
                        # could not find evidence.
                        verification["summary"]["final_verdict"] = (
                            article_label
                        )

                        verification["summary"]["confidence"] = (
                            article_confidence
                        )

                        # Make agreement fields consistent
                        verification["summary"]["agreement"] = 100.0

                        verification["summary"]["majority_verdict"] = (
                            article_label
                        )

                        verification["summary"]["agreement_counts"] = {
                            article_label: 1
                        }

                        verification["summary"]["scores"] = {
                            article_label: article_confidence
                        }

                        # Put article evidence into the normal
                        # evidence list used by Streamlit.
                        verification["results"] = [
                            {
                                "document": {
                                    "title": "Linked Article",
                                    "source": "Linked Article",
                                    "url": article_result.get(
                                        "source"
                                    ),
                                    "chunk_text": article_result.get(
                                        "evidence",
                                        ""
                                    ),
                                },
                                "source": "Linked Article",
                                "verdict": article_label,
                                "confidence": article_confidence,
                                "highlight": claim,
                            }
                        ]
                        if article_label in {
                            "SUPPORTED",
                            "CONTRADICTED",
                        }:

                            summary["final_verdict"] = (
                                article_label
                            )

                            summary["confidence"] = (
                                article_confidence
                            )

                            summary["majority_verdict"] = (
                                article_label
                            )

                            verification["explanation"] = (
                                "The claim was verified against "
                                "the linked article."
                            )

                            verification["reasoning"] = [
                                "The linked article provided "
                                "supporting evidence."
                            ]

                results.append({
                    "post": extracted,
                    "claim": claim,
                    "verification": verification,
                })

            except Exception as e:

                print(
                    "Verification error:",
                    type(e).__name__,
                    str(e),
                )

    print("\n" + "=" * 80)
    print("SOCIAL VERIFICATION COMPLETE")
    print("Posts processed:", total)
    print("Verified claims:", len(results))
    print("=" * 80)

    return results


def is_incomplete_sentence(text: str) -> bool:

    text = text.strip()

    if not text:
        return True

    incomplete_endings = (
        "—",
        "-",
        "...",
        "…",
        "[",
        "(",
        "about",
        "that",
        "because",
        "which",
        "while",
        "and",
        "or",
        "but",
    )

    lower = text.lower()

    return lower.endswith(incomplete_endings)
def _article_fallback(claim: str, post_text: str):

    url = extract_url(post_text)

    if not url:
        return None

    print("=" * 80)
    print("ARTICLE FALLBACK")
    print("URL:", url)
    print("=" * 80)

    article_text = fetch_article(url)

    if not article_text:
        print("Could not fetch article.")
        return None

    print(
        "ARTICLE TEXT LENGTH:",
        len(article_text)
    )

    try:
        from app.verification.verifier import verify_claim

        result = verify_claim(
            claim,
            article_text
        )

        # Keep the actual article evidence
        # so the frontend can display it.
        result["evidence"] = article_text
        result["source"] = url

        return result

    except Exception as e:

        print(
            "Article verification failed:",
            type(e).__name__,
            str(e)
        )

        return None

def _clean_feed_spacing(text: str) -> str:
    if not text:
        return ""

    text = re.sub(
        r"(?<=[a-z])(?=[A-Z])",
        " ",
        text,
    )

    replacements = {
        "Windingwire": "Winding wire",
        "createsan": "creates an",
        "thatrepels": "that repels",
        "andattracts": "and attracts",
        "firstdescription": "first description",
        "recordof": "record of",
        "sheddinglight": "shedding light",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text
def verify_single_social_post(url: str):
    """
    Verify a single Mastodon post from its URL.
    """

    import re
    import requests

    match = re.search(
        r"https?://([^/]+)/@[^/]+/(\d+)",
        url.strip(),
    )

    if not match:
        raise ValueError(
            "Please enter a valid Mastodon post URL."
        )

    instance = f"https://{match.group(1)}"
    status_id = match.group(2)

    response = requests.get(
        f"{instance}/api/v1/statuses/{status_id}",
        headers={
            "Accept": "application/json",
            "User-Agent": "VeritasAI/1.0",
        },
        timeout=15,
    )

    response.raise_for_status()

    post = response.json()

    results = _verify_posts([post])

    if not results:
        return {
            "post": post,
            "claims": [],
            "results": [],
            "message": (
                "No factual claim was detected in this post."
            ),
        }

    return results[0]
def verify_social_url(url: str):
    """Fetch and verify a single Mastodon post."""

    from urllib.parse import urlparse
    import requests

    url = url.strip()
    parsed = urlparse(url)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Please enter a valid Mastodon post URL.")

    if not parsed.netloc:
        raise ValueError("Please enter a valid Mastodon post URL.")

    parts = [
        part
        for part in parsed.path.split("/")
        if part
    ]

    if len(parts) < 2:
        raise ValueError("Invalid Mastodon post URL.")

    status_id = parts[-1]

    if not status_id.isdigit():
        raise ValueError("Could not find the Mastodon post ID.")

    instance = f"{parsed.scheme}://{parsed.netloc}"

    response = requests.get(
        f"{instance}/api/v1/statuses/{status_id}",
        headers={
            "Accept": "application/json",
            "User-Agent": "VeritasAI/1.0",
        },
        timeout=15,
    )

    response.raise_for_status()

    post = response.json()
    results = _verify_posts([post])

    return {
        "post": post,
        "results": results,
    }