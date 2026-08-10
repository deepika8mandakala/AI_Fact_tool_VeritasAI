import streamlit as st


def show_source_badge(
    source: str,
    score: float | None = None,
):

    # =====================================================
    # Source Without Credibility Score
    # =====================================================

    if score is None:

        st.markdown(
            f"""
            🔗 **{source}**

            *Source linked directly from the submitted post*
            """
        )

        return

    # =====================================================
    # Scored Source
    # =====================================================

    score = max(
        0.0,
        min(float(score), 1.0)
    )

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

        *{label}*
        """
    )