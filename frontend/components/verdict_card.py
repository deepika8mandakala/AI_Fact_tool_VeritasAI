import streamlit as st


def show_verdict(summary):

    verdict = summary.get(
        "final_verdict",
        "INSUFFICIENT_EVIDENCE"
    )

    confidence = summary.get(
        "confidence",
        0.0
    )

    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
        confidence = 0.0

    confidence = max(
        0.0,
        min(confidence, 1.0)
    )

    # =====================================================
    # Verdict
    # =====================================================

    if verdict == "SUPPORTED":

        st.success(
            "🟢 SUPPORTED"
        )

    elif verdict == "CONTRADICTED":

        st.error(
            "🔴 CONTRADICTED"
        )

    else:

        st.warning(
            "🟡 INSUFFICIENT EVIDENCE"
        )

    # =====================================================
    # Confidence
    # =====================================================

    if verdict == "INSUFFICIENT_EVIDENCE":

        st.info(
            "🎯 Confidence: Not enough evidence "
            "to determine whether the claim is true or false."
        )

    else:

        st.progress(
            confidence,
            text=f"Confidence: {confidence:.1%}"
        )

    # =====================================================
    # Conflict Detection
    # =====================================================

    if summary.get(
        "conflict",
        False
    ):

        st.warning(
            "⚠️ Conflicting evidence detected. "
            "Different sources disagree."
        )

    # =====================================================
    # Verification Statistics
    # =====================================================

    agreement = summary.get(
        "agreement"
    )

    majority = summary.get(
        "majority_verdict"
    )

    counts = summary.get(
        "agreement_counts",
        {}
    )

    has_statistics = (
        agreement is not None
        or majority is not None
        or bool(counts)
    )

    if not has_statistics:
        return

    st.markdown("---")

    st.subheader(
        "📊 Verification Summary"
    )

    # =====================================================
    # Agreement + Majority
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        agreement_value = (
            float(agreement)
            if agreement is not None
            else 0.0
        )

        st.metric(
            "Evidence Agreement",
            f"{agreement_value:.1f}%"
        )

    with col2:

        st.metric(
            "Majority Verdict",
            majority or verdict
        )

    # =====================================================
    # Evidence Distribution
    # =====================================================

    if counts:

        st.markdown(
            "**Evidence Distribution**"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "🟢 Supported",
                counts.get(
                    "SUPPORTED",
                    0
                )
            )

        with col2:

            st.metric(
                "🔴 Contradicted",
                counts.get(
                    "CONTRADICTED",
                    0
                )
            )

        with col3:

            st.metric(
                "🟡 Insufficient",
                counts.get(
                    "INSUFFICIENT_EVIDENCE",
                    0
                )
            )