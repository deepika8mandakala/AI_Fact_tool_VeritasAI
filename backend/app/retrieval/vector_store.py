import faiss
import numpy as np
import pickle
from pathlib import Path

# =====================================================
# Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]

VECTOR_DB = BASE_DIR / "vector_db"
VECTOR_DB.mkdir(exist_ok=True)

INDEX_PATH = VECTOR_DB / "faiss.index"
METADATA_PATH = VECTOR_DB / "metadata.pkl"

# =====================================================
# FAISS
# =====================================================

DIMENSION = 384

index = faiss.IndexFlatIP(DIMENSION)

metadata = []

# =====================================================
# Add Documents
# =====================================================

def add_documents(embeddings, docs):
    global metadata

    embeddings = np.asarray(
        embeddings,
        dtype=np.float32
    )

    index.add(embeddings)

    metadata.extend(docs)

# =====================================================
# Search
# =====================================================

def search(query_embedding, top_k=5):

    if index.ntotal == 0:
        print("FAISS index is empty.")
        return []

    query_embedding = np.asarray(
        [query_embedding],
        dtype=np.float32
    )

    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        if idx >= len(metadata):
            continue

        results.append(
            {
                "score": float(score),
                "document": metadata[idx]
            }
        )

    return results

# =====================================================
# Save
# =====================================================

def save():

    faiss.write_index(
        index,
        str(INDEX_PATH)
    )

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print(f"Saved FAISS index -> {INDEX_PATH}")
    print(f"Saved metadata -> {METADATA_PATH}")
    print(f"Vectors: {index.ntotal}")
    print(f"Metadata: {len(metadata)}")

# =====================================================
# Load
# =====================================================

def load():

    global index
    global metadata

    if INDEX_PATH.exists():

        index = faiss.read_index(
            str(INDEX_PATH)
        )

        print(
            f"Loaded FAISS index with {index.ntotal} vectors"
        )

    else:

        print(
            f"FAISS index not found at {INDEX_PATH}"
        )

    if METADATA_PATH.exists():

        with open(METADATA_PATH, "rb") as f:
            metadata = pickle.load(f)

        print(
            f"Loaded {len(metadata)} metadata records"
        )

    else:

        print(
            f"Metadata not found at {METADATA_PATH}"
        )

# =====================================================
# Debug
# =====================================================

if __name__ == "__main__":

    load()

    print("\n===== DEBUG =====")
    print("Index Path :", INDEX_PATH)
    print("Metadata Path :", METADATA_PATH)
    print("Vectors :", index.ntotal)
    print("Metadata :", len(metadata))

    if metadata:
        print("\nFirst document:")
        print(metadata[0])