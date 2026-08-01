from pydantic import BaseModel
from typing import List, Dict, Any


class SummaryResponse(BaseModel):

    final_verdict: str

    confidence: float

    scores: Dict[str, float]

    # -------------------------
    # Agreement Engine
    # -------------------------

    agreement: float = 0.0

    majority_verdict: str = "INSUFFICIENT_EVIDENCE"

    agreement_counts: Dict[str, int] = {}

    # -------------------------
    # Conflict Detection
    # -------------------------

    conflict: bool = False


class VerificationResponse(BaseModel):

    claim: str

    summary: SummaryResponse

    explanation: str

    reasoning: List[str]

    filtered_out: int

    results: List[Dict[str, Any]]