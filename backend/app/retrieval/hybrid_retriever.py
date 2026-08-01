from app.retrieval.service import retrieve_evidence
from app.retrieval.web_retriever import wikipedia_search
from app.retrieval.wikidata_retriever import wikidata_search
from app.retrieval.classifier import is_news_claim
from app.ranking.service import rank_evidence
from app.filtering.relevance import (
    filter_relevant_evidence
)
SIMILARITY_THRESHOLD = 0.70


def hybrid_retrieve(claim: str, top_k: int):

    faiss_result = retrieve_evidence(
        claim,
        top_k
    )

    similarity = faiss_result["max_similarity"]

    evidence = []

    news = is_news_claim(claim)

    print("News Claim:", news)
    print("Similarity:", similarity)

    # -------------------------
    # News claims
    # -------------------------

    if news:

        print("Using News Index")

        evidence.extend(
            faiss_result["evidence"]
        )

    # -------------------------
    # Fact claims
    # -------------------------

    else:

        if similarity >= SIMILARITY_THRESHOLD:

            print("High similarity -> Using FAISS")

            evidence.extend(
                faiss_result["evidence"]
            )

        else:

            print("Low similarity -> Using Wikipedia")

            wiki_results = wikipedia_search(claim)

            for item in wiki_results:

                item["retrieval_score"] = 1.0

            wiki_results = rank_evidence(
                claim,
                wiki_results
            )

            evidence.extend(
                wiki_results
            )

            wikidata = wikidata_search(claim)

            if wikidata:

                for item in wikidata:

                    item["retrieval_score"] = 1.0

                wikidata = rank_evidence(
                    claim,
                    wikidata
                )

                evidence.extend(
                    wikidata
                )

    # -------------------------
    # Remove duplicates
    # -------------------------

    unique = {}

    for item in evidence:

        key = (
            item["document"]["doc_id"],
            item["document"]["chunk_id"]
        )

        unique[key] = item

    evidence = list(
        unique.values()
    )

    evidence = filter_relevant_evidence(
        claim,
        evidence
    )
    print(
        "Relevant Evidence:",
        len(evidence)
    )
    faiss_result["evidence"] = evidence

    return faiss_result