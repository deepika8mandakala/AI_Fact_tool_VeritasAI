from fastapi import APIRouter, HTTPException
from app.database.crud import (
    get_claim_history,
    get_statistics,
    delete_history,
)

from app.schemas.analytics import (
    HistoryResponse,
    StatisticsResponse,
    DeleteHistoryResponse,
)

router = APIRouter()


@router.get(
    "/history",
    summary="Get Claim History",
    response_model=HistoryResponse
)
def history():
    try:
        history = get_claim_history()

        return {
            "total": len(history),
            "history": history
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/stats",
    summary="Get Verification Statistics",
    response_model=StatisticsResponse
)
def stats():
    try:
        return get_statistics()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/history",
    summary="Delete Verification History",
    response_model=DeleteHistoryResponse
)
def clear_history():
    try:
        delete_history()

        return {
            "message": "Verification history deleted successfully."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))