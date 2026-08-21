from fastapi import APIRouter
from typing import Any
from app.claim_detection.service import detect_claims
from app.url.schemas import URLVerificationRequest
from app.url.service import extract_article
from app.verification.pipeline import verify_pipeline

router = APIRouter(
    prefix="/url",
    tags=["URL Verification"]
)


@router.post(
    "/verify",
    response_model=dict[str, Any]
)
def verify_url(request: URLVerificationRequest):

    article = extract_article(request.url)
    print("=" * 80)
    print("TITLE:", article["title"])
    print("TEXT LENGTH:", len(article["text"]))
    print(article["text"][:1000])   # first 1000 characters
    print("=" * 80)

    claims = detect_claims(article["text"])

    print("=" * 80)
    print("CLAIMS FOUND:", claims["total_claims"])
    print("=" * 80)

    results = []

    for item in claims["claims"]:

        try:

            verification = verify_pipeline(
                item["claim"],
                request.top_k
            )

            verification["claim_confidence"] = item["confidence"]
            verification["entities"] = item["entities"]

            results.append(verification)

        except Exception as e:

            import traceback

            print("=" * 80)
            print("ERROR VERIFYING CLAIM")
            print(item["claim"])
            traceback.print_exc()
            print("=" * 80)

    # Sort by verification confidence
    results.sort(
        key=lambda x: x["summary"]["confidence"],
        reverse=True
    )

    return {
        "url": request.url,
        "title": article["title"],
        "authors": article["authors"],
        "publish_date": article["publish_date"],
        "total_claims": claims["total_claims"],
        "verified_claims": results[:3]      # show only top3
    }
