import streamlit as st
import pandas as pd

from utils import (
    get_history,
    clear_history
)


def show_history():

    st.header("Verification History")

    history = get_history()

    rows = []
    confidence = []

    if history["history"]:

        for item in history["history"]:

            rows.append(
                {
                    "Claim": item["claim"],
                    "Verdict": item["verdict"],
                    "Confidence": item["confidence"]
                }
            )

            confidence.append(
                item["confidence"]
            )

        df = pd.DataFrame(rows)

        st.data_editor(
            df,
            width="stretch",
            disabled=True,
            hide_index=True
        )

        csv = df.to_csv(index=False)

        st.download_button(
            label="📥 Download Verification History",
            data=csv,
            file_name="verification_history.csv",
            mime="text/csv",
            width="stretch"
        )

    else:

        st.info(
            "No verification history available."
        )

    # Sidebar button

    if st.sidebar.button(
        "Clear History",
        key="clear_history"
    ):

        clear_history()

        st.success(
            "History cleared successfully."
        )

        st.rerun()

    return confidence