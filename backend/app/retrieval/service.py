from app.retrieval.retriever import retrieve
from app.retrieval.indexer import build_index
from app.ranking.service import rank_evidence


def create_index():
    return build_index()


def retrieve_evidence(claim: str, top_k: int = 10):

    retrieved = retrieve(claim, top_k)

    print("Retrieved:", len(retrieved))
    print(retrieved)

    for item in retrieved:
        item["retrieval_score"] = float(item.pop("score"))

    ranked = rank_evidence(claim, retrieved)

    print("Ranked:", len(ranked))
    print(ranked)

    max_similarity = max(
        (item["retrieval_score"] for item in ranked),
        default=0.0,
    )
    print("Maximum Similarity:", max_similarity)
    return {
        "claim": claim,
        "evidence": ranked,
        "max_similarity": max_similarity,
    }