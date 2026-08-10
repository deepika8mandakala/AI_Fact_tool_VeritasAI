from app.retrieval.service import retrieve_evidence
from app.retrieval.web_retriever import wikipedia_search
from app.retrieval.wikidata_retriever import wikidata_search
from app.retrieval.classifier import is_news_claim
from app.retrieval.news_retriever import latest_bbc_news
from app.ranking.service import rank_evidence
from app.filtering.relevance import filter_relevant_evidence

SIMILARITY_THRESHOLD = 0.90


def hybrid_retrieve(claim: str, top_k: int = 10):

    evidence = []

    news = is_news_claim(claim)

    print("=" * 80)
    print("News Claim:", news)
    print("=" * 80)

    # ==========================================================
    # NEWS CLAIMS
    # ==========================================================

    if news:
        print("News claim detected.")

        # --------------------------------------------------
        # 1. Retrieve local FAISS evidence
        # --------------------------------------------------

        faiss_result = retrieve_evidence(
            claim,
            top_k
        )

        similarity = faiss_result.get(
            "max_similarity",
            0.0
        )

        print("FAISS Similarity:", similarity)

        evidence.extend(
            faiss_result.get(
                "evidence",
                []
            )
        )

        # --------------------------------------------------
        # 2. Retrieve current BBC news
        # --------------------------------------------------

        print("Loading Live BBC News...")

        articles = latest_bbc_news()

        live_news = []

        for article in articles:

            summary = article.get(
                "summary",
                ""
            )

            title = article.get(
                "title",
                ""
            )

            text = (
                f"{title}. "
                f"{summary}"
            ).strip()

            if not text:
                continue

            document = {
                "doc_id": article["url"],
                "chunk_id": 0,
                "title": title,
                "source": "BBC",
                "url": article["url"],
                "published_at": None,
                "chunk_text": text,
            }

            live_news.append({
                "document": document,
                "retrieval_score": 0.0
            })

        # --------------------------------------------------
        # 3. Cross-encoder ranking
        # --------------------------------------------------

        if live_news:

            live_news = rank_evidence(
                claim,
                live_news
            )

            print("=" * 80)
            print("BBC RANKING")
            print("=" * 80)

            for item in live_news:

                print(
                    item["document"]["title"],
                    "| Rerank:",
                    round(
                        item.get(
                            "rerank_score",
                            0.0
                        ),
                        3
                    )
                )

            evidence.extend(live_news)

    # ==========================================================
    # UNIVERSAL / FACT CLAIMS
    # ==========================================================

    else:

        print("Using Wikipedia + Wikidata")

        wiki_results = wikipedia_search(claim)

        print("Wikipedia Results:", len(wiki_results))

        for item in wiki_results:
            item["retrieval_score"] = 1.0

        wiki_results = rank_evidence(
            claim,
            wiki_results
        )

        evidence.extend(wiki_results)

        wikidata = wikidata_search(claim)

        if wikidata:

            for item in wikidata:
                item["retrieval_score"] = 1.0

            wikidata = rank_evidence(
                claim,
                wikidata
            )

            evidence.extend(wikidata)

        faiss_result = {
            "claim": claim,
            "evidence": [],
            "max_similarity": 1.0
        }

    # ==========================================================
    # REMOVE DUPLICATES
    # ==========================================================

    unique = {}

    for item in evidence:

        key = (
            item["document"]["doc_id"],
            item["document"]["chunk_id"]
        )

        unique[key] = item

    evidence = list(unique.values())

    # ==========================================================
    # FILTER
    # ==========================================================

    evidence = filter_relevant_evidence(
        claim,
        evidence,
        threshold=0.20
    )

    print("=" * 80)
    print("Relevant Evidence:", len(evidence))
    print("=" * 80)

    faiss_result["evidence"] = evidence

    return faiss_result