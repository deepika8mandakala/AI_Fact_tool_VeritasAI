from fastapi import APIRouter
from pydantic import BaseModel

from app.verification.response_schema import VerificationResponse
from app.verification.pipeline import verify_pipeline
from app.verification.schemas import (
    VerificationRequest,
    BatchVerificationRequest,
)
from app.database.crud import save_claim
from app.social.service import verify_social_url
class SocialURLRequest(BaseModel):
    url: str
router = APIRouter(
    prefix="/verification",
    tags=["Claim Verification"]
)

@router.post(
    "/verify",
    response_model=VerificationResponse
)
def verify(request: VerificationRequest):

    result = verify_pipeline(
        request.claim,
        request.top_k
    )

    save_claim(
        claim=result["claim"],
        verdict=result["summary"]["final_verdict"],
        confidence=result["summary"]["confidence"],
        explanation=result["explanation"],
    )

    return result
@router.post("/social/verify")
def verify_social_post(request: SocialURLRequest):

    result = verify_social_url(
        request.url
    )

    if not result["results"]:
        return {
            "post": result["post"],
            "claims_found": 0,
            "results": [],
            "message": (
                "No factual claim was detected "
                "in this post."
            ),
        }

    for item in result["results"]:

        verification = item["verification"]
        summary = verification["summary"]

        save_claim(
            claim=item["claim"],
            verdict=summary["final_verdict"],
            confidence=summary["confidence"],
            explanation=verification["explanation"],
        )

    return {
        "post": result["post"],
        "claims_found": len(result["results"]),
        "results": result["results"],
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

            result = verify_pipeline(
                claim,
                request.top_k
            )

            summary = result["summary"]

            batch_results.append(
                {
                    "claim": claim,
                    "verdict": summary["final_verdict"],
                    "confidence": summary["confidence"],
                    "explanation": result["explanation"],
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