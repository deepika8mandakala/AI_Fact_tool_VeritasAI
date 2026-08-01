from fastapi import APIRouter
from app.verification.response_schema import VerificationResponse
from app.verification.aggregation import aggregate_verdict
from app.retrieval.service import retrieve_evidence
from app.explanation.service import generate_explanation
from app.filtering.service import filter_evidence
from app.retrieval.hybrid_retriever import hybrid_retrieve
from app.agreement.service import calculate_agreement
from app.verification.service import verify_evidence
from app.verification.schemas import (
    VerificationRequest,
    BatchVerificationRequest,
)

# NEW IMPORT
from app.database.crud import save_claim

router = APIRouter(
    prefix="/verification",
    tags=["Claim Verification"]
)

@router.post(
    "/verify",
    response_model=VerificationResponse
)
def verify(request: VerificationRequest):

    retrieved = hybrid_retrieve(
        request.claim,
        request.top_k
    )

    filtered = filter_evidence(
        retrieved["evidence"]
    )

    verified = verify_evidence(
        request.claim,
        filtered
    )
    agreement = calculate_agreement(
        verified
    )
    print("VERIFIED RESULTS:")
    from pprint import pprint
    pprint(verified)
    summary = aggregate_verdict(
        verified
    )
    summary["agreement"] = agreement["agreement"]

    summary["agreement_counts"] = agreement["counts"]

    summary["majority_verdict"] = agreement["majority"]

    explanation = generate_explanation(
        request.claim,
        summary,
        verified
    )

    # SAVE TO DATABASE
    save_claim(
        claim=request.claim,
        verdict=summary["final_verdict"],
        confidence=summary["confidence"],
        explanation=explanation["summary"],
    )

    return {
        "claim": request.claim,
        "summary": summary,
        "explanation": explanation["summary"],
        "reasoning": explanation["reasoning"],
        "filtered_out": len(retrieved["evidence"]) - len(filtered),
        "results": verified,
    }
# =====================================================
# Batch Verification
# =====================================================

@router.post("/verify-batch")
def verify_batch(request: BatchVerificationRequest):

    batch_results = []

    for claim in request.claims:

        try:

            # -------------------------
            # Retrieve evidence
            # -------------------------

            retrieved = hybrid_retrieve(
                claim,
                request.top_k
            )

            filtered = filter_evidence(
                retrieved["evidence"]
            )

            verified = verify_evidence(
                claim,
                filtered
            )

            summary = aggregate_verdict(
                verified
            )

            explanation = generate_explanation(
                claim,
                summary,
                verified
            )

            batch_results.append(
                {
                    "claim": claim,
                    "verdict": summary["final_verdict"],
                    "confidence": summary["confidence"],
                    "explanation": explanation["summary"],
                }
            )

        except Exception as e:

            batch_results.append(
                {
                    "claim": claim,
                    "verdict": "ERROR",
                    "confidence": 0.0,
                    "explanation": str(e),
                }
            )

    return {
        "total_claims": len(batch_results),
        "results": batch_results,
    }