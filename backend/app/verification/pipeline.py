from app.retrieval.hybrid_retriever import hybrid_retrieve
from app.filtering.service import filter_evidence
from app.verification.service import verify_evidence
from app.verification.aggregation import aggregate_verdict
from app.agreement.service import calculate_agreement
from app.explanation.service import generate_explanation


def verify_pipeline(claim: str, top_k: int = 5):

    print("=" * 80)
    print("PIPELINE RECEIVED:")
    print(repr(claim[:300]))
    print("Length:", len(claim))
    print("=" * 80)

    retrieved = hybrid_retrieve(
        claim,
        top_k
    )

    filtered = filter_evidence(
        retrieved["evidence"]
    )
    print("=" * 80)
    print("FILTERED EVIDENCE:", len(filtered))

    for item in filtered:
        print("TITLE:", item["document"]["title"])
        print("Retrieval:", item.get("retrieval_score"))
        print("Rerank:", item.get("rerank_score"))
        print("Relevance:", item.get("relevance_score"))
        print("-" * 60)

    print("=" * 80)
    verified = verify_evidence(
        claim,
        filtered
    )

    agreement = calculate_agreement(
        verified
    )

    summary = aggregate_verdict(
        verified
    )

    summary["agreement"] = agreement["agreement"]
    summary["agreement_counts"] = agreement["counts"]
    summary["majority_verdict"] = agreement["majority"]

    explanation = generate_explanation(
        claim,
        summary,
        verified
    )

    return {
        "claim": claim,
        "summary": summary,
        "explanation": explanation["summary"],
        "reasoning": explanation["reasoning"],
        "filtered_out": len(retrieved["evidence"]) - len(filtered),
        "results": verified,
    }