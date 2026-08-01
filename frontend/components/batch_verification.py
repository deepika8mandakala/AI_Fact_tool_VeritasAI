import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils import verify_batch


def show_batch_verification():

    st.markdown("---")

    st.header("📂 Batch Claim Verification")

    uploaded_file = st.file_uploader(
        "Upload a TXT or CSV file",
        type=["txt", "csv"],
        key="batch_upload"
    )

    batch_top_k = st.slider(
        "Top K Evidence",
        1,
        10,
        5,
        key="batch_slider"
    )

    claims = []

    if uploaded_file is not None:

        # -------------------------
        # TXT
        # -------------------------

        if uploaded_file.name.endswith(".txt"):

            text = uploaded_file.read().decode("utf-8")

            claims = [
                line.strip()
                for line in text.splitlines()
                if line.strip()
            ]

        # -------------------------
        # CSV
        # -------------------------

        elif uploaded_file.name.endswith(".csv"):

            df = pd.read_csv(uploaded_file)

            if "claim" not in df.columns:

                st.error(
                    "CSV must contain a column named 'claim'."
                )

                return

            claims = (
                df["claim"]
                .dropna()
                .astype(str)
                .tolist()
            )

        st.success(
            f"{len(claims)} claims loaded."
        )

        st.subheader("Preview")

        st.write(claims)

    # =======================================
    # Verify Button
    # =======================================

    if st.button(
        "🚀 Verify All Claims",
        key="verify_batch"
    ):

        if len(claims) == 0:

            st.warning(
                "Please upload a TXT or CSV first."
            )

            return

        with st.spinner(
            "Verifying claims..."
        ):

            result = verify_batch(
                claims,
                batch_top_k
            )

        batch_df = pd.DataFrame(
            result["results"]
        )

        # ==========================
        # Statistics
        # ==========================

        supported = (
            batch_df["verdict"]
            .eq("SUPPORTED")
            .sum()
        )

        contradicted = (
            batch_df["verdict"]
            .eq("CONTRADICTED")
            .sum()
        )

        insufficient = (
            batch_df["verdict"]
            .eq("INSUFFICIENT_EVIDENCE")
            .sum()
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Supported",
            supported
        )

        col2.metric(
            "Contradicted",
            contradicted
        )

        col3.metric(
            "Insufficient",
            insufficient
        )

        # ==========================
        # Pie Chart
        # ==========================

        fig, ax = plt.subplots()

        ax.pie(
            [
                supported,
                contradicted,
                insufficient
            ],
            labels=[
                "Supported",
                "Contradicted",
                "Insufficient"
            ],
            autopct="%1.1f%%",
            startangle=90
        )

        st.pyplot(fig)

        # ==========================
        # Results
        # ==========================

        st.subheader(
            "Verification Results"
        )

        st.data_editor(
            batch_df,
            hide_index=True,
            disabled=True,
            use_container_width=True
        )

        csv = batch_df.to_csv(
            index=False
        )

        st.download_button(
            "📥 Download Results",
            csv,
            "batch_results.csv",
            "text/csv",
            use_container_width=True
        )