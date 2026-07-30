"""
Source Credibility Ranking

Assigns a credibility score to evidence sources.
Higher score = More trusted source.
"""

from urllib.parse import urlparse


# Trusted domains and their credibility scores
SOURCE_SCORES = {

    # -----------------------------
    # International Organizations
    # -----------------------------
    "un.org": 1.00,
    "worldbank.org": 1.00,
    "who.int": 1.00,
    "oecd.org": 1.00,
    "imf.org": 1.00,

    # -----------------------------
    # Government Websites
    # -----------------------------
    "gov.in": 0.98,
    "gov.uk": 0.98,
    "usa.gov": 0.98,
    "nih.gov": 0.98,
    "cdc.gov": 0.98,
    "nasa.gov": 0.98,

    # -----------------------------
    # Encyclopedias
    # -----------------------------
    "wikipedia.org": 0.95,
    "wikidata.org": 0.95,
    "britannica.com": 0.95,

    # -----------------------------
    # International News
    # -----------------------------
    "reuters.com": 0.90,
    "apnews.com": 0.90,
    "bbc.com": 0.88,
    "bbc.co.uk": 0.88,
    "nytimes.com": 0.88,
    "theguardian.com": 0.87,

    # -----------------------------
    # Science & Medical
    # -----------------------------
    "nature.com": 0.96,
    "science.org": 0.96,
    "pubmed.ncbi.nlm.nih.gov": 0.98,

    # -----------------------------
    # Technology
    # -----------------------------
    "arxiv.org": 0.85,

    # -----------------------------
    # Financial
    # -----------------------------
    "bloomberg.com": 0.87,
    "wsj.com": 0.87,

    # -----------------------------
    # Default News Blogs
    # -----------------------------
    "medium.com": 0.60,
    "substack.com": 0.60,
}


DEFAULT_SCORE = 0.60


def get_source_score(url: str) -> float:
    """
    Returns credibility score for a URL.

    Parameters
    ----------
    url : str

    Returns
    -------
    float
        Credibility score (0-1)
    """

    if not url:
        return DEFAULT_SCORE

    try:
        domain = urlparse(url).netloc.lower()

        # Remove www.
        if domain.startswith("www."):
            domain = domain[4:]

        # Exact match
        if domain in SOURCE_SCORES:
            return SOURCE_SCORES[domain]

        # Parent domain match
        for trusted_domain, score in SOURCE_SCORES.items():
            if domain.endswith(trusted_domain):
                return score

    except Exception:
        pass

    return DEFAULT_SCORE