import streamlit as st


def show_verdict(summary):

    verdict = summary["final_verdict"]

    score = summary["confidence"]

    if verdict == "SUPPORTED":

        st.success("🟢 SUPPORTED")

    elif verdict == "CONTRADICTED":

        st.error("🔴 CONTRADICTED")

    else:

        st.warning("🟡 INSUFFICIENT EVIDENCE")

    score = max(0.0, min(score, 1.0))

    st.progress(score)

    st.write(
        f"Confidence: {score:.2%}"
    )