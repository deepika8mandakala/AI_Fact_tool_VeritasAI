from app.ranking.reranker import rerank


def rank_evidence(claim: str, evidence: list):

    ranked = rerank(claim, evidence)

    return ranked[:5]