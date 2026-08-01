import streamlit as st


def show_metrics(result):

    summary = result["summary"]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Evidence",
        len(result["results"])
    )

    c2.metric(
        "Filtered",
        result["filtered_out"]
    )

    c3.metric(
        "Confidence",
        f"{summary['confidence']*100:.1f}%"
    )

    # -------------------------
    # Agreement (only if present)
    # -------------------------

    if "agreement" in summary:

        st.markdown("---")

        st.subheader("Evidence Agreement")

        col1, col2 = st.columns(2)

        col1.metric(
            "Agreement",
            f"{summary.get('agreement', 0)}%"
        )

        col2.metric(
            "Majority",
            summary.get(
                "majority_verdict",
                summary["final_verdict"]
            )
        )

        st.write("Evidence Distribution")

        st.json(
            summary.get(
                "agreement_counts",
                {}
            )
        )