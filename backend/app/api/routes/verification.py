from fastapi import APIRouter
from app.verification.response_schema import VerificationResponse
from app.verification.aggregation import aggregate_verdict
from app.retrieval.service import retrieve_evidence
from app.verification.schemas import VerificationRequest
from app.verification.service import verify_evidence
from app.explanation.service import generate_explanation
from app.filtering.service import filter_evidence
from app.retrieval.hybrid_retriever import hybrid_retrieve


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
    print("VERIFIED RESULTS:")
    from pprint import pprint
    pprint(verified)
    summary = aggregate_verdict(
        verified
    )

    explanation = generate_explanation(
        request.claim,
        summary,
        verified
    )

    # SAVE TO DATABASE
    # save_claim(
    #    claim=request.claim,
    #   verdict=summary["final_verdict"],
    #    confidence=summary["confidence"],
    #   explanation=explanation,
    # )

    return {
        "claim": request.claim,
        "summary": summary,
        "explanation": explanation,
        "filtered_out": len(retrieved["evidence"]) - len(filtered),
        "results": verified,
    }