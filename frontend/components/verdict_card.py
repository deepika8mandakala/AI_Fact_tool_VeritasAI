import streamlit as st


def show_verdict(summary):

    verdict = summary["final_verdict"]

    score = summary["confidence"]

    # -------------------------
    # Verdict
    # -------------------------

    if verdict == "SUPPORTED":

        st.success("🟢 SUPPORTED")

    elif verdict == "CONTRADICTED":

        st.error("🔴 CONTRADICTED")

    else:

        st.warning("🟡 INSUFFICIENT EVIDENCE")

    # -------------------------
    # Confidence
    # -------------------------

    score = max(0.0, min(score, 1.0))

    st.progress(score)

    st.write(
        f"**Confidence:** {score:.2%}"
    )

    # -------------------------
    # Conflict Detection
    # -------------------------

    if summary.get("conflict", False):

        st.warning(
            "⚠️ **Conflicting evidence detected.** "
            "Different evidence sources disagree with each other."
        )

    # -------------------------
    # Agreement
    # -------------------------

    if "agreement" in summary:

        st.markdown("---")

        col1, col2 = st.columns(2)

        col1.metric(
            "Agreement",
            f"{summary['agreement']}%"
        )

        col2.metric(
            "Majority",
            summary.get(
                "majority_verdict",
                verdict
            )
        )

    # -------------------------
    # Evidence Counts
    # -------------------------

    if "agreement_counts" in summary:

        st.subheader("Evidence Distribution")

        counts = summary["agreement_counts"]

        st.write(
            f"🟢 Supported: {counts.get('SUPPORTED', 0)}"
        )

        st.write(
            f"🔴 Contradicted: {counts.get('CONTRADICTED', 0)}"
        )

        st.write(
            f"🟡 Insufficient: {counts.get('INSUFFICIENT_EVIDENCE', 0)}"
        )