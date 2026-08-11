from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.retrieval.vector_store import load
from app.api.router import api_router
from app.database.db import Base, engine
from app.database import models
from app.url.router import router as url_router
from app.pdf.router import router as pdf_router
from app.image.router import router as image_router


Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):

    print(
        "Starting VeritasAI...",
        flush=True,
    )

    load()

    print(
        "VeritasAI startup complete.",
        flush=True,
    )

    yield


app = FastAPI(
    title="Veritas AI API",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)
app.include_router(pdf_router)
app.include_router(url_router)
app.include_router(image_router)


@app.get("/")
def home():

    return {
        "message": "Veritas AI Backend Running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }