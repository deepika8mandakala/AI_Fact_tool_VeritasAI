import streamlit as st
from components.source_badge import show_source_badge
from utils.source_logos import SOURCE_LOGOS
from components.trust_gauge import (
    show_trust_gauge
)

def show_evidence_card(evidence):

    doc = evidence["document"]

    verdict = evidence.get(
        "verdict",
        "UNKNOWN"
    )

    # =====================================================
    # Card Header
    # =====================================================

    if verdict == "SUPPORTED":

        st.success(f"✅ {doc['title']}")

    elif verdict == "CONTRADICTED":

        st.error(f"❌ {doc['title']}")

    else:

        st.warning(f"⚠️ {doc['title']}")

    # =====================================================
    # Source Information
    # =====================================================

    source = doc.get(
        "source",
        "Unknown"
    )

    logo = SOURCE_LOGOS.get(source)

    col1, col2 = st.columns([1, 6])

    with col1:

        if logo:

            try:

                st.image(
                    logo,
                    width=40
                )

            except Exception:

                pass

    with col2:

        show_source_badge(
            source,
            evidence.get(
                "source_score",
                0.60
            )
        )

    # =====================================================
    # Freshness
    # =====================================================

    freshness = evidence.get(
        "freshness_score",
        0.50
    )

    st.markdown(
        f"**🕒 Freshness:** {freshness:.2f}"
    )

    st.markdown("---")

    # =====================================================
    # Quality
    # =====================================================

    stars = evidence.get(
        "stars",
        0
    )

    quality = evidence.get(
        "quality_score",
        0
    )

    label = evidence.get(
        "quality_label",
        "Unknown"
    )

    st.markdown(
        f"### {'⭐' * stars}"
    )

    st.markdown(
        f"**🏆 Quality Score:** {quality:.1f}"
    )

    st.markdown(
        f"**🏷️ Quality:** {label}"
    )

    # =====================================================
    # Credibility Information
    # =====================================================

    show_trust_gauge(
        evidence.get(
            "source_score",
            0.60
        )
    )

    st.markdown(
        f"**⚖️ Bias:** {evidence.get('bias', 'Unknown')}"
    )

    st.markdown(
        f"**🛡️ Reliability:** {evidence.get('reliability', 'Unknown')}"
    )

    st.markdown(
        f"**📂 Category:** {evidence.get('category', 'Unknown')}"
    )

    st.markdown(
        f"**📅 Published:** {doc.get('published_at', 'N/A')}"
    )

    # =====================================================
    # Scores
    # =====================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Confidence",
            f"{evidence.get('confidence', 0.0) * 100:.1f}%"
        )

    with col2:

        st.metric(
            "Retrieval",
            f"{evidence.get('retrieval_score', 0.0):.3f}"
        )

    with col3:

        st.metric(
            "Rerank",
            f"{evidence.get('rerank_score', 0.0):.3f}"
        )

    # =====================================================
    # Highlight
    # =====================================================

    st.markdown("### 🔍 Evidence")

    st.info(
        evidence.get(
            "highlight",
            "No supporting evidence available."
        )
    )

    # =====================================================
    # Original Article
    # =====================================================

    url = doc.get("url")

    if url:

        st.markdown(
            f"🔗 [Open Original Article]({url})"
        )

    st.divider()