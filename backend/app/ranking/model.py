from sentence_transformers import CrossEncoder  # type: ignore

MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

ranking_model = CrossEncoder(MODEL_NAME)