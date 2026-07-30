from pydantic import BaseModel
from typing import List, Dict, Any


class SummaryResponse(BaseModel):
    final_verdict: str
    confidence: float
    scores: Dict[str, float]


class VerificationResponse(BaseModel):
    claim: str
    summary: SummaryResponse
    explanation: str
    filtered_out: int
    results: List[Dict[str, Any]]