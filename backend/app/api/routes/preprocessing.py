from fastapi import APIRouter
from pydantic import BaseModel

from app.preprocessing.service import preprocess_document


router = APIRouter(
    prefix="/preprocessing",
    tags=["Preprocessing"]
)


class TextRequest(BaseModel):
    text: str


@router.post("/clean")
def preprocess(request: TextRequest):

    return preprocess_document(request.text)