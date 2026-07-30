import faiss
import numpy as np
import pickle
import os

INDEX_PATH = "vector_db/faiss.index"
METADATA_PATH = "vector_db/metadata.pkl"

dimension = 384

index = faiss.IndexFlatIP(dimension)

metadata = []


def add_documents(embeddings, docs):

    global metadata

    embeddings = np.asarray(
        embeddings,
        dtype=np.float32
    )
    index.add(embeddings)

    metadata.extend(docs)


def search(query_embedding, top_k=5):

    query_embedding = np.array(
        [query_embedding],
        dtype="float32"
    )

    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        results.append(
            {
                "score": float(score),
                "document": metadata[idx]
            }
        )

    return results


def save():

    os.makedirs("vector_db", exist_ok=True)

    faiss.write_index(
        index,
        INDEX_PATH
    )

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)


def load():

    global index
    global metadata

    if os.path.exists(INDEX_PATH):

        index = faiss.read_index(INDEX_PATH)

    if os.path.exists(METADATA_PATH):

        with open(METADATA_PATH, "rb") as f:
            metadata = pickle.load(f)