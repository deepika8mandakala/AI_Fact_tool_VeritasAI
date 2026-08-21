from sentence_transformers import CrossEncoder

MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

ranking_model = CrossEncoder(
    MODEL_NAME,
    max_length=512,
    trust_remote_code=True
)