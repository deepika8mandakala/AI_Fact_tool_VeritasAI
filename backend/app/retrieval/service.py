from app.retrieval.retriever import retrieve
from app.retrieval.indexer import build_index
from app.ranking.service import rank_evidence


def create_index():
    return build_index()


def retrieve_evidence(claim: str, top_k: int = 10):

    # -------------------------
    # Retrieve from FAISS
    # -------------------------
    retrieved = retrieve(claim, top_k)

    print("Retrieved:", len(retrieved))
    print(retrieved)

    # -------------------------
    # Rename score
    # -------------------------
    for item in retrieved:
        item["retrieval_score"] = float(
            item.pop("score")
        )

    # -------------------------
    # Rank evidence
    # -------------------------
    ranked = rank_evidence(
        claim,
        retrieved
    )

    # -------------------------
    # Remove duplicate URLs
    # -------------------------
    unique = []
    seen = set()

    for item in ranked:

        url = item["document"]["url"]

        if url in seen:
            continue

        seen.add(url)
        unique.append(item)

    ranked = unique

    print("Ranked:", len(ranked))
    print(ranked)

    # -------------------------
    # Maximum similarity
    # -------------------------
    max_similarity = max(
        (
            item["retrieval_score"]
            for item in ranked
        ),
        default=0.0,
    )

    print("Maximum Similarity:", max_similarity)

    return {
        "claim": claim,
        "evidence": ranked,
        "max_similarity": max_similarity,
    }