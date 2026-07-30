from app.ingestion.service import collect_all_sources
from app.preprocessing.service import preprocess_documents

from app.retrieval.chunker import chunk_text
from app.retrieval.embedding import get_embeddings
from app.retrieval.vector_store import add_documents, save


def build_index():
    """
    Fetch articles from all sources, preprocess them,
    split into chunks, generate embeddings,
    and store them in FAISS.
    """

    print("\n========== BUILDING VECTOR INDEX ==========\n")

    # Step 1: Fetch articles
    print("Fetching articles...")
    articles = collect_all_sources()

    print(f"Fetched {len(articles)} articles")

    if not articles:
        return {
            "success": False,
            "message": "No articles fetched from ingestion sources.",
            "indexed_documents": 0
        }

    # Step 2: Preprocess articles
    print("Preprocessing articles...")
    processed = preprocess_documents(articles)

    # Remove empty articles
    processed = [
        article
        for article in processed
        if article.get("clean_text", "").strip()
    ]

    print(f"Articles after preprocessing: {len(processed)}")

    if not processed:
        return {
            "success": False,
            "message": "No valid articles after preprocessing.",
            "indexed_documents": 0
        }

    # Step 3: Chunk articles
    print("Creating chunks...")

    documents = []

    for article in processed:

        chunks = chunk_text(article["clean_text"])

        for idx, chunk in enumerate(chunks):

            if not chunk.strip():
                continue

            documents.append(
                {
                    "doc_id": article["url"],
                    "chunk_id": idx,
                    "title": article["title"],
                    "source": article["source"],
                    "url": article["url"],
                    "published_at": article.get("published_at", ""),
                    "chunk_text": chunk
                }
            )

    print(f"Generated {len(documents)} chunks")

    if not documents:
        return {
            "success": False,
            "message": "No chunks were generated.",
            "indexed_documents": 0
        }

    # Step 4: Generate embeddings
    print("Generating embeddings...")

    embeddings = get_embeddings(
        [doc["chunk_text"] for doc in documents]
    )

    print(f"Generated {len(embeddings)} embeddings")

    # Step 5: Store in FAISS
    print("Adding vectors to FAISS...")

    add_documents(
        embeddings,
        documents
    )

    save()

    print("\nVector index saved successfully.")
    print("===========================================\n")

    return {
        "success": True,
        "message": "Index built successfully.",
        "articles_processed": len(processed),
        "indexed_documents": len(documents)
    }