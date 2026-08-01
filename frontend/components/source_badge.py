import streamlit as st


def show_source_badge(source: str, score: float):

    if score >= 0.90:
        color = "🟢"
        stars = "★★★★★"
        label = "Highly Trusted"

    elif score >= 0.75:
        color = "🟡"
        stars = "★★★★☆"
        label = "Trusted"

    elif score >= 0.60:
        color = "🟠"
        stars = "★★★☆☆"
        label = "Moderately Trusted"

    else:
        color = "🔴"
        stars = "★★☆☆☆"
        label = "Low Trust"

    st.markdown(
        f"""
{color} **{source}**

{stars}

**Credibility:** {score:.2f}

_{label}_
"""
    )