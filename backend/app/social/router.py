from fastapi import APIRouter
from pydantic import BaseModel

from app.social.live_monitor import (
    start_monitor,
    stop_monitor,
    get_status,
    get_results,
    clear_results,
)


router = APIRouter(
    prefix="/social/live",
    tags=["Live Social Verification"],
)


class LiveMonitorRequest(BaseModel):

    hashtag: str


# =========================================================
# Start
# =========================================================

@router.post("/start")
def start_live_monitor(
    request: LiveMonitorRequest,
):

    return start_monitor(
        request.hashtag
    )


# =========================================================
# Stop
# =========================================================

@router.post("/stop")
def stop_live_monitor():

    return stop_monitor()


# =========================================================
# Status
# =========================================================

@router.get("/status")
def live_monitor_status():

    return get_status()


# =========================================================
# Results
# =========================================================

@router.get("/results")
def live_monitor_results():

    return {
        "results": get_results()
    }


# =========================================================
# Clear
# =========================================================

@router.delete("/results")
def clear_live_results():

    return clear_results()