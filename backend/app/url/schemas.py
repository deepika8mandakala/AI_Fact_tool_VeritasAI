from pydantic import BaseModel


class URLVerificationRequest(BaseModel):

    url: str

    top_k: int = 5