from app.retrieval.retrieval_config import FAISS_THRESHOLD


def should_use_external_sources(max_similarity: float) -> bool:
    """
    Decide whether Wikipedia/Wikidata should be queried.
    """
    return max_similarity < FAISS_THRESHOLD