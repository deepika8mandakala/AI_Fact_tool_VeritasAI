import streamlit as st
import matplotlib.pyplot as plt

from utils import get_stats


def show_analytics():

    st.sidebar.title("Analytics")

    try:

        stats = get_stats()

    except Exception:

        stats = {
            "total_claims": 0,
            "supported": 0,
            "contradicted": 0,
            "insufficient_evidence": 0
        }

    # ==========================
    # Sidebar Metrics
    # ==========================

    st.sidebar.metric(
        "Total Claims",
        stats["total_claims"]
    )

    st.sidebar.metric(
        "Supported",
        stats["supported"]
    )

    st.sidebar.metric(
        "Contradicted",
        stats["contradicted"]
    )

    st.sidebar.metric(
        "Insufficient",
        stats["insufficient_evidence"]
    )

    labels = [
        "Supported",
        "Contradicted",
        "Insufficient"
    ]

    values = [
        stats["supported"],
        stats["contradicted"],
        stats["insufficient_evidence"]
    ]

    # ==========================
    # Bar Chart
    # ==========================

    st.subheader("Verdict Distribution")

    if sum(values) > 0:

        fig, ax = plt.subplots()

        ax.bar(labels, values)

        ax.set_ylabel("Number of Claims")

        st.pyplot(fig)

        fig, ax = plt.subplots()

        ax.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90
        )

        ax.set_title("Verdict Distribution")

        st.pyplot(fig)

    else:

        st.info("No analytics available.")

    return stats