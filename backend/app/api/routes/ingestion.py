from fastapi import APIRouter
from app.ingestion.newsapi import fetch_news
from app.ingestion.rss import fetch_rss
from app.ingestion.service import collect_all_sources

router = APIRouter(
    prefix="/ingestion",
    tags=["Ingestion"]
)


@router.get("/news")
def get_news(query: str):
    return fetch_news(query)


@router.get("/rss")
def get_rss():
    return fetch_rss()


@router.get("/all")
def get_all(query: str):
    return collect_all_sources(query)