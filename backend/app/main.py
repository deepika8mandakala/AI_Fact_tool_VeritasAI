from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.retrieval.vector_store import load
from app.api.router import api_router
from app.database.db import Base, engine
from app.database import models

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Veritas AI API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.on_event("startup")
def startup():

    load()


@app.get("/")
def home():
    return {
        "message": "Veritas AI Backend Running"
    }