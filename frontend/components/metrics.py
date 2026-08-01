import streamlit as st

def show_metrics(result):

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
        f"{result['summary']['confidence']*100:.1f}%"
    )