from fastapi import APIRouter

from app.api.routes.ingestion import router as ingestion_router
from app.api.routes.preprocessing import router as preprocessing_router
from app.api.routes.entity import router as entity_router
from app.api.routes.claims import router as claims_router
from app.api.routes.retrieval import router as retrieval_router
from app.api.routes.verification import router as verification_router
from app.analytics.routes import router as analytics_router

api_router = APIRouter()

api_router.include_router(ingestion_router)
api_router.include_router(preprocessing_router)
api_router.include_router(entity_router)
api_router.include_router(claims_router)
api_router.include_router(retrieval_router)
api_router.include_router(verification_router)
api_router.include_router(
    analytics_router,
    prefix="/analytics",
    tags=["Analytics"]
)