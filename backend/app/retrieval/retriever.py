from app.retrieval.embedding import get_embedding
from app.retrieval.vector_store import search


def retrieve(
    claim: str,
    top_k: int = 5
):

    embedding = get_embedding(claim)

    results = search(
    embedding,
    top_k
)
    return sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )