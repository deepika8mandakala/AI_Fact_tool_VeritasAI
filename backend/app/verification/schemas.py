from pydantic import BaseModel


# ===============================
# Single Claim Verification
# ===============================

class VerificationRequest(BaseModel):

    claim: str
    top_k: int = 10


# ===============================
# Batch Verification
# ===============================

class BatchVerificationRequest(BaseModel):

    claims: list[str]

    top_k: int = 10