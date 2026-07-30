from app.retrieval.retriever import retrieve
from app.retrieval.indexer import build_index
from app.ranking.service import rank_evidence


def create_index():
    return build_index()


def retrieve_evidence(claim: str, top_k: int = 10):

    retrieved = retrieve(
        claim,
        top_k
    )

    # Convert FAISS score -> retrieval_score
    for item in retrieved:
        item["retrieval_score"] = float(item.pop("score"))

    ranked = rank_evidence(
        claim,
        retrieved
    )

    return {
        "claim": claim,
        "evidence": ranked
    }