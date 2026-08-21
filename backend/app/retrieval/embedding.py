from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-small-en-v1.5"

_embedding_model = None


def get_embedding_model():
    """
    Lazily load the embedding model.

    The model is loaded only when an embedding is actually
    required, rather than during FastAPI application startup.
    """

    global _embedding_model

    if _embedding_model is None:

        print(
            "Loading embedding model...",
            flush=True,
        )

        _embedding_model = SentenceTransformer(
            MODEL_NAME,
            device="cpu",
        )

        print(
            "Embedding model loaded.",
            flush=True,
        )

    return _embedding_model


def get_embedding(text: str):
    """
    Generate an embedding for a single text.
    """

    model = get_embedding_model()

    return model.encode(
        text,
        normalize_embeddings=True,
    )


def get_embeddings(texts: list[str]):
    """
    Generate embeddings for multiple texts.
    """

    model = get_embedding_model()

    return model.encode(
        texts,
        normalize_embeddings=True,
    )