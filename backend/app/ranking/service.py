from app.ranking.reranker import rerank


def rank_evidence(claim, evidence):

    return rerank(
        claim,
        evidence
    )