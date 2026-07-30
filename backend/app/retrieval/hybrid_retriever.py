from app.retrieval.service import retrieve_evidence
from app.retrieval.web_retriever import wikipedia_search
from app.retrieval.wikidata_retriever import wikidata_search
from app.classifier.claim_classifier import classify_claim


def hybrid_retrieve(claim: str, top_k: int):

    claim_type = classify_claim(claim)

    faiss_result = retrieve_evidence(claim, top_k)

    evidence = faiss_result["evidence"]

    if claim_type == "entity":

        evidence.extend(wikipedia_search(claim))

        wikidata_results = wikidata_search(claim) or []

        evidence.extend(wikidata_results)

    elif claim_type == "scientific":

        evidence.extend(wikipedia_search(claim))

    elif claim_type == "medical":

        evidence.extend(wikipedia_search(claim))

    elif claim_type == "statistical":

        evidence.extend(wikipedia_search(claim))

    faiss_result["evidence"] = evidence

    return faiss_result