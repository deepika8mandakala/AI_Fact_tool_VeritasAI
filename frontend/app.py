import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils import (
    verify_claim,
    get_history,
    get_stats,
    clear_history
)

from components.verdict_card import show_verdict
from components.evidence_card import show_evidence_card
from components.metrics import show_metrics
from components.explanation_card import show_explanation
st.set_page_config(
    page_title="VeritasAI",
    layout="wide"
)

st.title("🛡️ VeritasAI")

# ==========================
# SIDEBAR ANALYTICS
# ==========================

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
# VERDICT BAR CHART
# ==========================

st.subheader("Verdict Distribution")

if sum(values) > 0:

    fig, ax = plt.subplots()

    ax.bar(labels, values)

    ax.set_ylabel("Number of Claims")

    st.pyplot(fig)

else:

    st.info("No verification data available for the bar chart.")

# ==========================
# PIE CHART
# ==========================

if sum(values) > 0:

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

    st.info("No verification data available for the pie chart.")

# ==========================
# CLAIM VERIFICATION
# ==========================

st.subheader("Real-Time Claim Verification")

claim = st.text_area(
    "📝 Enter a claim to verify",
    placeholder="Example: Narendra Modi is the Prime Minister of India",
    height=120
)

top_k = st.slider(
    "Top K Evidence",
    1,
    10,
    5
)

if st.button("Verify Claim"):

    if not claim.strip():

        st.warning("Please enter a claim.")

        st.stop()

    with st.spinner("🔍 Searching trusted sources and verifying the claim..."):

        try:

            result = verify_claim(
                claim,
                top_k
            )

        except Exception as e:

            st.error(str(e))

            st.stop()

    st.success("Verification Complete")

    summary = result["summary"]

    verdict = summary["final_verdict"]

    show_verdict(summary)
    show_metrics(result)

    show_explanation(result)


    st.header("Evidence")

    for evidence in result["results"]:

        show_evidence_card(
            evidence
        )

# ==========================
# HISTORY
# ==========================

st.header("Verification History")

history = get_history()

rows = []

confidence = []

if history["history"]:

    for item in history["history"]:

        rows.append({
            "Claim": item["claim"],
            "Verdict": item["verdict"],
            "Confidence": item["confidence"]
        })

        confidence.append(
            item["confidence"]
        )

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True
    )

    csv = df.to_csv(
        index=False
    )

    st.download_button(
        label="📥 Download Verification History",
        data=csv,
        file_name="verification_history.csv",
        mime="text/csv",
        use_container_width=True
    )

else:

    st.info(
        "No verification history available."
    )

# ==========================
# CONFIDENCE HISTOGRAM
# ==========================

if confidence:

    st.subheader(
        "Confidence Distribution"
    )

    fig, ax = plt.subplots()

    ax.hist(
        confidence,
        bins=10
    )

    ax.set_xlabel(
        "Confidence"
    )

    ax.set_ylabel(
        "Frequency"
    )

    st.pyplot(fig)

# ==========================
# CLEAR HISTORY
# ==========================

if st.sidebar.button("Clear History"):

    clear_history()

    st.sidebar.success(
        "History cleared successfully."
    )

    st.rerun()