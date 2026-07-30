from pydantic import BaseModel


class Article(BaseModel):
    title: str
    source: str
    url: str
    published_at: str = ""
    clean_text: str
    language: str = "en"