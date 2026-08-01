"""
Source Credibility Ranking
"""

from urllib.parse import urlparse

SOURCE_INFO = {

    # -----------------------------
    # International Organizations
    # -----------------------------
    "un.org": {
        "score": 1.00,
        "bias": "None",
        "reliability": "Very High",
        "category": "International Organization"
    },

    "worldbank.org": {
        "score": 1.00,
        "bias": "None",
        "reliability": "Very High",
        "category": "International Organization"
    },

    "who.int": {
        "score": 1.00,
        "bias": "None",
        "reliability": "Very High",
        "category": "Health"
    },

    "gov.in": {
        "score": 0.98,
        "bias": "Low",
        "reliability": "Very High",
        "category": "Government"
    },

    "bbc.com": {
        "score": 0.88,
        "bias": "Low",
        "reliability": "High",
        "category": "International News"
    },

    "bbc.co.uk": {
        "score": 0.88,
        "bias": "Low",
        "reliability": "High",
        "category": "International News"
    },

    "reuters.com": {
        "score": 0.90,
        "bias": "Low",
        "reliability": "Very High",
        "category": "International News"
    },

    "apnews.com": {
        "score": 0.90,
        "bias": "Low",
        "reliability": "Very High",
        "category": "International News"
    },

    "wikipedia.org": {
        "score": 0.95,
        "bias": "Low",
        "reliability": "High",
        "category": "Encyclopedia"
    },

    "wikidata.org": {
        "score": 0.95,
        "bias": "Low",
        "reliability": "High",
        "category": "Knowledge Base"
    },

    "nature.com": {
        "score": 0.96,
        "bias": "None",
        "reliability": "Very High",
        "category": "Scientific Journal"
    },
    "economictimes.indiatimes.com": {
    "score": 0.84,
    "bias": "Low",
    "reliability": "High",
    "category": "Business News"
},

    "onefootball.com": {
        "score": 0.75,
        "bias": "Low",
        "reliability": "Medium",
        "category": "Sports"
    },

    "financialpost.com": {
        "score": 0.85,
        "bias": "Low",
        "reliability": "High",
        "category": "Business News"
    },

    "science.org": {
        "score": 0.96,
        "bias": "None",
        "reliability": "Very High",
        "category": "Scientific Journal"
    },

    "pubmed.ncbi.nlm.nih.gov": {
        "score": 0.98,
        "bias": "None",
        "reliability": "Very High",
        "category": "Medical Research"
    },

    "medium.com": {
        "score": 0.60,
        "bias": "Unknown",
        "reliability": "Medium",
        "category": "Blog"
    },

    "substack.com": {
        "score": 0.60,
        "bias": "Unknown",
        "reliability": "Medium",
        "category": "Blog"
    },

    "thehindu.com": {
    "score": 0.88,
    "bias": "Low",
    "reliability": "High",
    "category": "National News"
    },

}

DEFAULT_INFO = {
    "score": 0.60,
    "bias": "Unknown",
    "reliability": "Medium",
    "category": "Unknown"
}


def get_source_info(url: str):

    if not url:
        return DEFAULT_INFO

    try:

        domain = urlparse(url).netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        if domain in SOURCE_INFO:
            return SOURCE_INFO[domain]

        for trusted_domain, info in SOURCE_INFO.items():
            if domain.endswith(trusted_domain):
                return info

    except Exception:
        pass

    return DEFAULT_INFO


def get_source_score(url: str) -> float:
    """
    Backward compatible.
    Existing code still works.
    """
    return get_source_info(url)["score"]