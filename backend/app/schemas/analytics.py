from pydantic import BaseModel
from typing import List


class ClaimHistoryResponse(BaseModel):
    id: int
    claim: str
    verdict: str
    confidence: float
    explanation: str


class HistoryResponse(BaseModel):
    total: int
    history: List[ClaimHistoryResponse]


class StatisticsResponse(BaseModel):
    total_claims: int
    supported: int
    contradicted: int
    insufficient_evidence: int


class DeleteHistoryResponse(BaseModel):
    message: str