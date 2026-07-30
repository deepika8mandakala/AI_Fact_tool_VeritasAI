from pydantic import BaseModel


class VerificationRequest(BaseModel):

    claim: str
    top_k: int = 10