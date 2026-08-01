from app.ranking.reranker import rerank


def rank_evidence(claim, evidence):

    for item in evidence:
        item["rerank_score"] = item["retrieval_score"]
        item["source_score"] = 0.8
        item["final_score"] = item["retrieval_score"]

    return evidence[:5]