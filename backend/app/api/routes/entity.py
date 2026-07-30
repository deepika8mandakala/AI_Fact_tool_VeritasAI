from fastapi import APIRouter
from pydantic import BaseModel

from app.entity_recognition.service import process_entities

router = APIRouter(
    prefix="/entity",
    tags=["Named Entity Recognition"]
)


class TextRequest(BaseModel):
    text: str


@router.post("/extract")
def extract(request: TextRequest):

    return process_entities(request.text)