from typing import Dict


def create_evidence(
    document: Dict,
    retrieval_score: float,
    retriever: str,
):
    """
    Standard evidence format used by all retrievers.
    """

    return {
        "document": document,
        "retrieval_score": retrieval_score,
        "retriever": retriever,
    }