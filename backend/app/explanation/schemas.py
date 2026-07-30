from pydantic import BaseModel


class ExplanationResponse(BaseModel):

    explanation: str