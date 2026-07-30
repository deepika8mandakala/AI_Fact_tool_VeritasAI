from pydantic import BaseModel


class RetrievalRequest(BaseModel):

    claim: str

    top_k: int = 5