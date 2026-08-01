import streamlit as st

from utils import verify_claim

from components.verdict_card import show_verdict
from components.metrics import show_metrics
from components.explanation_card import show_explanation
from components.evidence_card import show_evidence_card


def show_single_verification():

    st.subheader("Real-Time Claim Verification")

    claim = st.text_area(
        "📝 Enter a claim to verify",
        placeholder="Example: Narendra Modi is the Prime Minister of India",
        height=120,
        key="single_claim"
    )

    top_k = st.slider(
        "Top K Evidence",
        1,
        10,
        5,
        key="single_top_k"
    )

    if st.button(
        "Verify Claim",
        key="verify_single"
    ):

        if not claim.strip():

            st.warning(
                "Please enter a claim."
            )

            return

        with st.spinner(
            "🔍 Searching trusted sources..."
        ):

            try:

                result = verify_claim(
                    claim,
                    top_k
                )

            except Exception as e:

                st.error(str(e))

                return

        st.success(
            "Verification Complete"
        )

        summary = result["summary"]

        show_verdict(summary)

        show_metrics(result)

        show_explanation(result)

        st.header("Evidence")

        for evidence in result["results"]:

            show_evidence_card(
                evidence
            )