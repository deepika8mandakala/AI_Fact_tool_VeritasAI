from fastapi import APIRouter
from pydantic import BaseModel

from app.claim_detection.service import detect_claims

router = APIRouter(
    prefix="/claims",
    tags=["Claim Detection"]
)

class ClaimRequest(BaseModel):
    text: str

@router.post("/extract")
def extract_claims(request: ClaimRequest):
    return detect_claims(request.text)