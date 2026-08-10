from app.retrieval.retriever import retrieve
from app.retrieval.indexer import build_index
from app.ranking.service import rank_evidence


def create_index():
    return build_index()


def retrieve_evidence(claim: str, top_k: int = 10):

    # -------------------------
    # Retrieve from FAISS
    # -------------------------
    # Improve retrieval for very short claims
    query = claim.strip()

    if len(query.split()) < 15:
        query = f"{claim}. {claim}"

    retrieved = retrieve(query, max(top_k, 10))
    print("="*80)
    print("TOP RETRIEVED DOCUMENTS")

    for i, item in enumerate(retrieved[:5], 1):
        print(f"\n{i}.", item["document"]["title"])
        print(item["score"])
        print(item["document"]["chunk_text"][:200])

    print("="*80)

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

        key = (
            item["document"]["url"],
            item["document"]["chunk_id"]
        )

        if key in seen:
            continue

        seen.add(key)
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