import streamlit as st
from components.source_badge import show_source_badge

def show_evidence_card(evidence):

    doc = evidence["document"]

    verdict = evidence["verdict"]

    # -----------------------------
    # Card Header
    # -----------------------------
    if verdict == "SUPPORTED":
        st.success(f"✅ {doc['title']}")

    elif verdict == "CONTRADICTED":
        st.error(f"❌ {doc['title']}")

    else:
        st.warning(f"⚠️ {doc['title']}")

    # -----------------------------
    # Source Information
    # -----------------------------
    show_source_badge(
    doc["source"],
    evidence["source_score"]
)
    st.markdown(f"**📅 Published:** {doc.get('published_at', 'N/A')}")

    # -----------------------------
    # Scores
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Confidence",
            f"{evidence['confidence']*100:.1f}%"
        )

    with col2:
        st.metric(
            "Retrieval",
            f"{evidence['retrieval_score']:.3f}"
        )

    with col3:
        st.metric(
            "Rerank",
            f"{evidence['rerank_score']:.3f}"
        )

    # -----------------------------
    # Evidence
    # -----------------------------
    st.markdown("### 🔍 Evidence")

    st.info(evidence["highlight"])

    # -----------------------------
    # Original Article
    # -----------------------------
    url = doc.get("url")

    if url:
        st.markdown(f"🔗 [Open Original Article]({url})")

    st.divider()