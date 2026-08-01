import streamlit as st


def show_trust_gauge(score: float):

    score = max(0.0, min(score, 1.0))

    st.markdown("### 🛡 Trust Score")

    st.progress(score)

    percent = score * 100

    if percent >= 90:
        label = "🟢 Highly Trusted"

    elif percent >= 75:
        label = "🟢 Trusted"

    elif percent >= 60:
        label = "🟠 Moderately Trusted"

    else:
        label = "🔴 Low Trust"

    st.markdown(
        f"## {percent:.0f}%"
    )

    st.write(label)