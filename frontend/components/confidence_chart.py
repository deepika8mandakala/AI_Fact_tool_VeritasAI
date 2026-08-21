import streamlit as st
import matplotlib.pyplot as plt


def show_confidence_chart(confidence):

    if not confidence:
        return

    st.subheader("Confidence Distribution")

    fig, ax = plt.subplots()

    ax.hist(
        confidence,
        bins=10
    )

    ax.set_xlabel("Confidence")

    ax.set_ylabel("Frequency")

    ax.set_title("Confidence Histogram")

    st.pyplot(fig)