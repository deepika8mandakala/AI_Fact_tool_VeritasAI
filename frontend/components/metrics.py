import streamlit as st


def show_metrics(result):

    summary = result.get(
        "summary",
        {}
    )

    evidence_count = len(
        result.get(
            "results",
            []
        )
    )

    filtered_count = result.get(
        "filtered_out",
        0
    )

    confidence = summary.get(
        "confidence",
        0.0
    )

    confidence = max(
        0.0,
        min(float(confidence), 1.0)
    )

    # =====================================================
    # Core Metrics
    # =====================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📚 Evidence",
            evidence_count
        )

    with col2:

        st.metric(
            "🔎 Filtered",
            filtered_count
        )

    with col3:

        st.metric(
            "🎯 Confidence",
            f"{confidence:.1%}"
        )