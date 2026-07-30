from fastapi import APIRouter

from app.retrieval.schemas import RetrievalRequest
from app.retrieval.service import (
    retrieve_evidence,
    create_index
)

router = APIRouter(
    prefix="/retrieval",
    tags=["Evidence Retrieval"]
)


@router.post("/index")
def index_articles():

    return create_index()


@router.post("/search")
def search(request: RetrievalRequest):

    return retrieve_evidence(
        request.claim,
        request.top_k
    )