from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-small-en-v1.5"

embedding_model = SentenceTransformer(MODEL_NAME)


def get_embedding(text: str):
    """
    Generate embedding for a single text.
    """
    return embedding_model.encode(
        text,
        normalize_embeddings=True
    )


def get_embeddings(texts: list[str]):
    """
    Generate embeddings for multiple texts.
    """
    return embedding_model.encode(
        texts,
        normalize_embeddings=True
    )