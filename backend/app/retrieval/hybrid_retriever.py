from app.retrieval.service import retrieve_evidence
from app.retrieval.web_retriever import wikipedia_search
from app.retrieval.wikidata_retriever import wikidata_search
from app.classifier.claim_classifier import classify_claim

SIMILARITY_THRESHOLD = 0.70


def hybrid_retrieve(claim: str, top_k: int):

    claim_type = classify_claim(claim)

    faiss_result = retrieve_evidence(claim, top_k)

    evidence = []

    # Use FAISS only if similarity is high
    if faiss_result["max_similarity"] < SIMILARITY_THRESHOLD:
        print("Low similarity -> Using Wikipedia")

        evidence.extend(faiss_result["evidence"])

    else:

        print("Low similarity -> Using Wikipedia")

    # Wikipedia fallback
    if claim_type in [
        "entity",
        "scientific",
        "medical",
        "statistical"
    ]:

        evidence.extend(
            wikipedia_search(claim)
        )

        wikidata = wikidata_search(claim)

        if wikidata:
            evidence.extend(wikidata)

    # Remove duplicates
    unique = {}

    for item in evidence:

        key = (
            item["document"]["doc_id"],
            item["document"]["chunk_id"]
        )

        unique[key] = item

    faiss_result["evidence"] = list(unique.values())

    return faiss_result