from app.retrieval.retriever import retrieve
from app.retrieval.indexer import build_index
from app.ranking.service import rank_evidence


def create_index():
    return build_index()


def retrieve_evidence(claim: str, top_k: int = 10):

    retrieved = retrieve(claim, top_k)

    # Convert FAISS score -> retrieval_score
    for item in retrieved:
        item["retrieval_score"] = float(item.pop("score"))

    # IMPORTANT: rerank the evidence
    ranked = rank_evidence(claim, retrieved)

    max_similarity = max(
        (item["retrieval_score"] for item in ranked),
        default=0.0,
    )
    print(ranked[0].keys() if ranked else "No evidence")
    return {
        "claim": claim,
        "evidence": ranked,
        "max_similarity": max_similarity,
    }