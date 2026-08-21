import streamlit as st

from components.source_badge import show_source_badge
from assets.source_logos import SOURCE_LOGOS


def show_evidence_card(evidence):

    doc = evidence.get(
        "document",
        {}
    )

    verdict = evidence.get(
        "verdict",
        "UNKNOWN"
    )

    title = doc.get(
        "title",
        "Evidence Source"
    )

    source = doc.get(
        "source",
        "Unknown"
    )

    # =====================================================
    # Card Header
    # =====================================================

    if verdict == "SUPPORTED":

        st.success(
            f"✅ {title}"
        )

    elif verdict == "CONTRADICTED":

        st.error(
            f"❌ {title}"
        )

    else:

        st.warning(
            f"⚠️ {title}"
        )

    # =====================================================
    # Source Information
    # =====================================================

    logo = SOURCE_LOGOS.get(source)

    col1, col2 = st.columns(
        [1, 6]
    )

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
            evidence.get("source_score")
        )

    # =====================================================
    # Verification Result
    # =====================================================

    confidence = evidence.get(
        "confidence",
        0.0
    )

    st.markdown(
        f"**Verification:** {verdict}"
    )

    st.markdown(
        f"**Confidence:** {confidence * 100:.1f}%"
    )

    # =====================================================
    # Evidence Text
    # =====================================================

    st.markdown(
        "### 🔍 Evidence"
    )

    highlight = evidence.get(
        "highlight"
    )

    if highlight:

        st.info(
            highlight
        )

    else:

        chunk_text = doc.get(
            "chunk_text",
            ""
        )

        if chunk_text:

            st.info(
                chunk_text
            )

        else:

            st.info(
                "No supporting evidence text available."
            )

    # =====================================================
    # Source URL
    # =====================================================

    url = doc.get(
        "url"
    )

    if url:

        st.markdown(
            f"🔗 [Open Original Article]({url})"
        )

    st.divider()